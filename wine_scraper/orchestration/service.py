"""Refactored wine scraper service with proper message handling."""

import asyncio
import json
from typing import Optional

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from config.settings import settings
from scrapers.winery import WineryScraper
from pipelines.models import Wine
from utils.observability import get_logger

logger = get_logger("wine-service")


class WineScraperService:
    """Refactored wine scraper service with proper message handling."""

    def __init__(self):
        self.connection_url = f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:{settings.rabbitmq_port}/"
        self.consumer_queue = settings.rabbitmq_wineries_queue
        self.exchange_name = settings.rabbitmq_wines_exchange
        self.routing_key = settings.rabbitmq_wine_scraped_routing_key
        self.connection: Optional[aio_pika.abc.AbstractConnection] = None
        self.channel: Optional[aio_pika.abc.AbstractChannel] = None
        self.consumer_queue_obj: Optional[aio_pika.abc.AbstractQueue] = None
        self.exchange: Optional[aio_pika.abc.AbstractExchange] = None

    async def connect(self) -> None:
        """Establish connections to RabbitMQ."""
        try:
            self.connection = await aio_pika.connect_robust(self.connection_url, heartbeat=600)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)
            
            # Declare queues and exchange
            self.consumer_queue_obj = await self.channel.declare_queue(
                self.consumer_queue, durable=True, auto_delete=False
            )
            
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            
            # Bind wines queue to exchange
            wines_queue = await self.channel.declare_queue(
                "wines", durable=True, auto_delete=False
            )
            await wines_queue.bind(self.exchange, routing_key="wine.*")
            
            logger.info(f"Connected to RabbitMQ: consumer_queue={self.consumer_queue}, exchange={self.exchange_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def disconnect(self) -> None:
        """Close RabbitMQ connections."""
        if self.connection:
            await self.connection.close()
            logger.info("Disconnected from RabbitMQ")

    async def process_single_winery(self, winery_name: str, winery_url: str) -> list[Wine]:
        """Process a single winery with proper timeout handling."""
        try:
            logger.info(f"Starting scrape for {winery_name} ({winery_url})")
            
            scraper = WineryScraper(winery_name, winery_url)
            async with scraper:
                wines = await asyncio.wait_for(scraper.scrape_winery_site(), timeout=180.0)
                
            logger.info(f"Completed scrape for {winery_name}: {len(wines)} wines found")
            return wines
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout while scraping {winery_name}")
            return []
        except Exception as e:
            logger.error(f"Failed to scrape {winery_name}: {e}")
            return []

    async def publish_wines(self, wines: list[Wine]) -> None:
        """Publish wines to the wines exchange."""
        try:
            for wine in wines:
                message_body = json.dumps(wine.dict(), default=str)
                message = aio_pika.Message(
                    message_body.encode(),
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                )
                await self.exchange.publish(message, routing_key=self.routing_key)
                logger.debug(f"Published wine: {wine.name}")
            
            logger.info(f"Published {len(wines)} wines to exchange")
            
        except Exception as e:
            logger.error(f"Failed to publish wines: {e}")
            raise

    async def process_message(self, message: AbstractIncomingMessage) -> None:
        """Process a single message with immediate acknowledgment."""
        async with message.process():
            try:
                body_raw = message.body.decode()
                logger.debug(f"Raw message: {body_raw}")
                
                # Parse message
                try:
                    body = json.loads(body_raw)
                    if isinstance(body, str):
                        body = json.loads(body)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON format: {body_raw}")
                    return
                
                if not isinstance(body, dict):
                    logger.warning(f"Received non-dict message: {type(body)}")
                    return
                
                winery_name = body.get("name")
                winery_url = body.get("website") or body.get("url", "")
                
                if not winery_url or not winery_name:
                    logger.warning(f"Invalid message format: {body}")
                    return
                
                logger.info(f"Processing winery: {winery_name} ({winery_url})")
                
                # Scrape the winery (this happens after acknowledgment)
                wines = await self.process_single_winery(winery_name, winery_url)
                
                if wines:
                    await self.publish_wines(wines)
                    logger.info(f"Successfully processed {winery_name}: {len(wines)} wines")
                else:
                    logger.info(f"No wines found for {winery_name}")
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # Message is already acknowledged at this point
                logger.info("Message acknowledged despite processing error")

    async def run(self) -> None:
        """Run the service continuously."""
        await self.connect()
        
        try:
            logger.info("Starting wine scraper service...")
            print("Waiting for messages...")
            
            async with self.consumer_queue_obj.iterator() as queue_iter:
                async for message in queue_iter:
                    await self.process_message(message)
                    
        except Exception as e:
            logger.error(f"Service error: {e}")
            raise
        finally:
            await self.disconnect()

    async def run_once(self) -> None:
        """Run the service to process one message then exit."""
        await self.connect()
        
        try:
            message = await self.consumer_queue_obj.get(timeout=30)
            if message:
                await self.process_message(message)
                logger.info("Processed one message, exiting...")
            else:
                logger.info("No messages in queue")
                
        except asyncio.TimeoutError:
            logger.info("No messages to process")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            await self.disconnect()