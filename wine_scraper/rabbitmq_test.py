#!/usr/bin/env python3
"""Test script for writing wine data to RabbitMQ."""

import asyncio
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import aio_pika

class RabbitMQWineryScraper:
    def __init__(self, name, base_url, rabbitmq_url):
        self.name = name
        self.base_url = base_url
        self.rabbitmq_url = rabbitmq_url
    
    async def scrape_and_publish(self):
        """Scrape wines and publish to RabbitMQ."""
        print(f"🍷 Scraping {self.name} and publishing to RabbitMQ...")
        
        wines = await self.scrape_winery_site()
        
        if wines:
            await self.publish_to_rabbitmq(wines)
            print(f"✅ Published {len(wines)} wines to RabbitMQ")
        else:
            print("⚠️  No wines found to publish")
        
        return wines
    
    async def scrape_winery_site(self):
        """Scrape wines from the winery website."""
        wines = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                print(f"  Loading {self.base_url}...")
                await page.goto(self.base_url, wait_until="domcontentloaded", timeout=45000)
                await asyncio.sleep(2)
                
                # Get content
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Look for wine-related links
                wine_links = []
                
                # Check for shop links
                shop_links = soup.select("a[href*='shop'], a[href*='weine'], a[href*='produkte']")
                for link in shop_links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(self.base_url, href)
                        if 'shop' in full_url or 'weine' in full_url:
                            wine_links.append(full_url)
                
                # Also check main navigation
                nav_links = soup.select("nav a, .menu a, .navigation a")
                for link in nav_links:
                    href = link.get('href')
                    text = link.get_text().lower()
                    if href and ('wein' in text or 'shop' in text or 'sortiment' in text):
                        full_url = urljoin(self.base_url, href)
                        wine_links.append(full_url)
                
                wine_links = list(set(wine_links))[:5]
                print(f"  Found {len(wine_links)} potential wine pages")
                
                # Process wine pages
                for wine_url in wine_links:
                    try:
                        print(f"    Checking: {wine_url}")
                        await page.goto(wine_url, wait_until="domcontentloaded", timeout=20000)
                        
                        content = await page.content()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Extract wine data
                        title = soup.find('title')
                        title_text = title.text.strip() if title else "Unknown Wine"
                        
                        # Find wine products on the page
                        products = soup.select('.product-item, .wine-item, .shop-item')
                        
                        if not products:
                            # Try to find individual wine products
                            products = soup.select('[class*="product"], [class*="wine"]')
                        
                        for product in products:
                            # Extract wine name
                            name_elem = product.select_one('.product-title, .wine-name, h2, h3')
                            name = name_elem.get_text().strip() if name_elem else title_text
                            
                            # Skip if it's a category page
                            if any(skip in name.lower() for skip in ['weine', 'shop', 'sortiment', 'kategorie']):
                                continue
                            
                            # Extract price
                            price = None
                            price_elem = product.select_one('.price, [class*="price"]')
                            if price_elem:
                                price_text = price_elem.get_text()
                                price_match = re.search(r'(\d+(?:[.,]\d+)?)', price_text)
                                if price_match:
                                    price = float(price_match.group(1).replace(',', '.'))
                            
                            # Extract vintage
                            vintage = None
                            text = product.get_text() or soup.get_text()
                            year_match = re.search(r'\b(20[0-2][0-9]|19[5-9][0-9])\b', text)
                            if year_match:
                                year = int(year_match.group(1))
                                if 1950 <= year <= 2025:
                                    vintage = year
                            
                            if len(name) > 5 and name.lower() not in ['weingut', 'shop', 'kontakt']:
                                wine_data = {
                                    'name': name,
                                    'winery': self.name,
                                    'price': price,
                                    'vintage': vintage,
                                    'url': wine_url,
                                    'source': self.base_url
                                }
                                wines.append(wine_data)
                        
                        # If no products found, try to extract from page
                        if not wines:
                            # Look for wine titles and descriptions
                            wine_titles = soup.select('h1, h2, .product-title')
                            for title in wine_titles:
                                name = title.get_text().strip()
                                if len(name) > 10 and any(keyword in name.lower() for keyword in ['riesling', 'silvaner', 'burgunder']):
                                    wine_data = {
                                        'name': name,
                                        'winery': self.name,
                                        'price': price,
                                        'vintage': vintage,
                                        'url': wine_url,
                                        'source': self.base_url
                                    }
                                    wines.append(wine_data)
                    
                    except Exception as e:
                        print(f"    Error processing {wine_url}: {e}")
                        continue
                
                await browser.close()
                
            except Exception as e:
                print(f"Error accessing {self.base_url}: {e}")
                await browser.close()
        
        return wines
    
    async def publish_to_rabbitmq(self, wines):
        """Publish wines to RabbitMQ wines queue/exchange."""
        try:
            connection = await aio_pika.connect_robust(self.rabbitmq_url)
            async with connection:
                channel = await connection.channel()
                
                # Declare exchange
                exchange = await channel.declare_exchange(
                    "wines",
                    aio_pika.ExchangeType.TOPIC,
                    durable=True
                )
                
                # Publish each wine
                for wine in wines:
                    message_body = json.dumps(wine, ensure_ascii=False, indent=2)
                    message = aio_pika.Message(
                        message_body.encode(),
                        content_type="application/json",
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                    )
                    
                    await exchange.publish(message, routing_key="wine.scraped")
                    print(f"  📤 Published: {wine['name'][:50]}...")
                
                print(f"  📊 Published {len(wines)} wines to RabbitMQ exchange 'wines'")
                
        except Exception as e:
            print(f"❌ RabbitMQ Error: {e}")
            raise

async def test_rabbitmq_connection(rabbitmq_url):
    """Test RabbitMQ connection."""
    try:
        connection = await aio_pika.connect_robust(rabbitmq_url)
        await connection.close()
        print("✅ RabbitMQ connection successful")
        return True
    except Exception as e:
        print(f"❌ RabbitMQ connection failed: {e}")
        return False

async def main():
    """Main test function."""
    rabbitmq_url = "amqp://rabbitmq:rabbitmq@localhost:5672/"
    
    print("🍇 Starting RabbitMQ Winery Test")
    print("=" * 60)
    
    # Test RabbitMQ connection
    if not await test_rabbitmq_connection(rabbitmq_url):
        print("🔄 Starting in dry-run mode (no RabbitMQ)")
        print("To test with RabbitMQ, start RabbitMQ server:")
        print("  docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management")
        return
    
    wineries = [
        ('https://www.weingut-rainer-sauer.de/', 'Weingut Rainer Sauer'),
        ('https://www.buerklin-wolf.de/', 'Bürklin-Wolf'),
        ('https://www.leitz-wein.de/', 'Weingut Leitz')
    ]
    
    results = {}
    total_wines = 0
    
    for url, name in wineries:
        scraper = RabbitMQWineryScraper(name, url, rabbitmq_url)
        try:
            count = await scraper.scrape_and_publish()
            results[name] = count
            total_wines += count
        except Exception as e:
            print(f"❌ Failed {name}: {e}")
            results[name] = 0
    
    print("\n📊 RABBITMQ TEST SUMMARY")
    print("=" * 60)
    for name, count in results.items():
        status = "✅ PUBLISHED" if count > 0 else "❌ FAILED"
        print(f"{name}: {count} wines - {status}")
    
    print(f"\n🎯 TOTAL: {total_wines} wines published to RabbitMQ")
    
    success_count = sum(1 for c in results.values() if c > 0)
    success_rate = (success_count / len(wineries)) * 100
    print(f"📈 SUCCESS RATE: {success_count}/{len(wineries)} ({success_rate:.0f}%)")
    
    print(f"\n🔗 RabbitMQ connection: {rabbitmq_url}")
    print("📋 Exchange: 'wines' (Topic)")
    print("🎯 Routing key: 'wine.scraped'")

if __name__ == "__main__":
    asyncio.run(main())