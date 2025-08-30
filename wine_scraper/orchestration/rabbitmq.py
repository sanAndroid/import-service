"""RabbitMQ integration for winery queue processing."""

import asyncio
import json
from typing import Optional, List
from dataclasses import dataclass

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from config.settings import settings
from pipelines.models import Wine
from utils.observability import get_logger

logger = get_logger("rabbitmq")


@dataclass
class WineryMessage:
    """Message format from wineries queue."""
    website: str
    name: str


class RabbitMQConsumer:
    """RabbitMQ consumer for wineries queue."""

    def __init__(self):
        self.connection_url = f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:{settings.rabbitmq_port}/"
        self.queue_name = settings.rabbitmq_wineries_queue
        self.exchange_name = settings.rabbitmq_wines_exchange
        self.routing_key = settings.rabbitmq_winery_routing_key
        self.connection: Optional[aio_pika.abc.AbstractConnection] = None
        self.channel: Optional[aio_pika.abc.AbstractChannel] = None
        self.queue: Optional[aio_pika.abc.AbstractQueue] = None
        self.exchange: Optional[aio_pika.abc.AbstractExchange] = None

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        try:
            self.connection = await aio_pika.connect_robust(self.connection_url, heartbeat=600)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)

            # Declare the wineries queue for consuming
            self.queue = await self.channel.declare_queue(
                self.queue_name, durable=True, auto_delete=False
            )
            
            # Declare the wines exchange
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            
            # Bind wineries queue to winery routing key
            await self.queue.bind(self.exchange, routing_key=self.routing_key)
            
            # Declare and bind the wines queue to the wines exchange
            wines_queue = await self.channel.declare_queue(
                "wines", durable=True, auto_delete=False
            )
            await wines_queue.bind(self.exchange, routing_key="wine.*")
            
            logger.info(f"Connected to RabbitMQ: queue={self.queue_name}, exchange={self.exchange_name}")
            logger.info("Bound wines queue to wines exchange with routing key 'wine.*'")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def disconnect(self) -> None:
        """Close RabbitMQ connection."""
        if self.connection:
            await self.connection.close()
            logger.info("Disconnected from RabbitMQ")

    async def consume(self, callback) -> None:
        """Start consuming messages from the wineries queue."""
        if not self.connection or not self.queue:
            raise RuntimeError("Not connected to RabbitMQ")

        async def process_message(message: AbstractIncomingMessage) -> None:
            async with message.process():
                try:
                    body_raw = message.body.decode()
                    logger.debug(f"Raw message: {body_raw}")
                    
                    # Handle double-encoded JSON
                    try:
                        body = json.loads(body_raw)
                        if isinstance(body, str):
                            # Double-encoded JSON
                            body = json.loads(body)
                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON format: {body_raw}")
                        return
                    
                    if not isinstance(body, dict):
                        logger.warning(f"Received non-dict message: {type(body)} - {body}")
                        return
                    
                    # Handle null website values
                    website = body.get("website") or body.get("url", "")
                    if not website:
                        logger.warning(f"Received message with null/empty website for winery: {body.get('name', 'unknown')}")
                        return
                        
                    winery_msg = WineryMessage(website=website, name=body["name"])
                    logger.info(f"Processing winery: {winery_msg.name} ({winery_msg.website})")
                    await callback(winery_msg)
                except KeyError as e:
                    logger.error(f"Invalid message format: missing field {e}. Expected: {{\"name\":\"...\",\"website\":\"...\"}}")
                    logger.error(f"Received: {body_raw if 'body_raw' in locals() else 'unknown'}")
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in message: {e}")
                    logger.error(f"Raw message: {body_raw if 'body_raw' in locals() else message.body.decode()}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    logger.error(f"Message type: {type(body) if 'body' in locals() else 'unknown'}")

        await self.queue.consume(process_message)
        logger.info("Started consuming messages from wineries queue")


class RabbitMQProducer:
    """RabbitMQ producer for wines queue."""

    def __init__(self):
        self.connection_url = f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:{settings.rabbitmq_port}/"
        self.exchange_name = settings.rabbitmq_wines_exchange
        self.routing_key = settings.rabbitmq_wine_scraped_routing_key
        self.connection: Optional[aio_pika.abc.AbstractConnection] = None
        self.channel: Optional[aio_pika.abc.AbstractChannel] = None
        self.exchange: Optional[aio_pika.abc.AbstractExchange] = None

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        try:
            self.connection = await aio_pika.connect_robust(self.connection_url)
            self.channel = await self.connection.channel()
            
            # Declare the wines exchange
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            
            # Declare and bind the wines queue to the wines exchange
            wines_queue = await self.channel.declare_queue(
                "wines", durable=True, auto_delete=False
            )
            await wines_queue.bind(self.exchange, routing_key="wine.*")
            
            logger.info(f"Connected to RabbitMQ producer: exchange={self.exchange_name}")
            logger.info("Bound wines queue to wines exchange with routing key 'wine.*'")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ producer: {e}")
            raise

    async def disconnect(self) -> None:
        """Close RabbitMQ connection."""
        if self.connection:
            await self.connection.close()
            logger.info("Disconnected from RabbitMQ producer")

    async def publish_wines(self, wines: List[Wine]) -> None:
        """Publish wine data to the wines exchange."""
        if not self.connection or not self.exchange:
            raise RuntimeError("Not connected to RabbitMQ")

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


class RabbitMQManager:
    """Manages both consumer and producer connections."""

    def __init__(self):
        self.consumer = RabbitMQConsumer()
        self.producer = RabbitMQProducer()

    async def __aenter__(self):
        """Async context manager entry."""
        await self.consumer.connect()
        await self.producer.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.consumer.disconnect()
        await self.producer.disconnect()

    async def process_wineries(self, scraper_callback) -> None:
        """Process wineries from queue using the provided scraper callback."""
        await self.consumer.consume(scraper_callback)
