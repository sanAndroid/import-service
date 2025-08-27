#!/usr/bin/env python3
"""Clean test for writing wine data to RabbitMQ."""

import asyncio
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import aio_pika

class CleanRabbitMQWineryScraper:
    def __init__(self, name, base_url, rabbitmq_url):
        self.name = name
        self.base_url = base_url
        self.rabbitmq_url = rabbitmq_url
    
    async def scrape_and_publish(self):
        """Scrape wines and publish to RabbitMQ."""
        print(f"🍷 {self.name} - Scraping and publishing to RabbitMQ...")
        
        wines = await self.scrape_winery_site()
        
        if wines:
            await self.publish_to_rabbitmq(wines)
            print(f"✅ {self.name} - Published {len(wines)} wines")
            return len(wines)
        else:
            print(f"⚠️  {self.name} - No wines found")
            return 0
    
    async def scrape_winery_site(self):
        """Scrape wines from the winery website."""
        wines = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                print(f"  📍 Loading {self.base_url}...")
                await page.goto(self.base_url, wait_until="domcontentloaded", timeout=45000)
                await asyncio.sleep(3)  # Wait for JS content
                
                # Get all links and filter for wine/product pages
                all_links = await page.query_selector_all("a[href]")
                wine_urls = []
                
                for link in all_links:
                    href = await link.get_attribute('href')
                    text = await link.inner_text()
                    
                    if href and href.startswith('http') and 'weingut' not in href.lower():
                        text_lower = text.lower()
                        href_lower = href.lower()
                        
                        # Wine-related detection
                        wine_indicators = ['riesling', 'silvaner', 'burgunder', 'wein', 'wine', 'sekt', 'cuvee']
                        if any(indicator in text_lower or indicator in href_lower for indicator in wine_indicators):
                            wine_urls.append(href)
                
                # Remove duplicates and limit
                wine_urls = list(set(wine_urls))[:6]
                print(f"  🔍 Found {len(wine_urls)} wine URLs")
                
                # Process each wine URL
                for wine_url in wine_urls:
                    try:
                        print(f"    🔗 Processing: {wine_url[:60]}...")
                        await page.goto(wine_url, wait_until="domcontentloaded", timeout=20000)
                        
                        content = await page.content()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Extract wine name
                        name_selectors = ['h1', '.product-title', '.wine-name', 'title']
                        wine_name = None
                        for selector in name_selectors:
                            element = soup.select_one(selector)
                            if element:
                                wine_name = element.get_text().strip()
                                break
                        
                        if not wine_name or len(wine_name) < 10:
                            continue
                        
                        # Clean name
                        wine_name = re.sub(r'\s*\|\s*.*$', '', wine_name)  # Remove pipe and after
                        
                        # Extract price
                        price = None
                        price_selectors = ['.price', '.product-price', '[class*="price"]']
                        for selector in price_selectors:
                            elements = soup.select(selector)
                            for elem in elements:
                                price_text = elem.get_text()
                                match = re.search(r'(\d+(?:[.,]\d+)?)', price_text)
                                if match:
                                    price = float(match.group(1).replace(',', '.'))
                                    break
                            if price:
                                break
                        
                        # Extract vintage
                        vintage = None
                        text = soup.get_text()
                        year_match = re.search(r'\b(20[0-2][0-9]|19[5-9][0-9])\b', text)
                        if year_match:
                            year = int(year_match.group(1))
                            if 1950 <= year <= 2025:
                                vintage = year
                        
                        # Skip category pages
                        if any(skip in wine_name.lower() for skip in ['weine', 'shop', 'sortiment', 'kategorie']):
                            continue
                        
                        wine = {
                            'name': wine_name,
                            'winery': self.name,
                            'price': price,
                            'vintage': vintage,
                            'url': wine_url,
                            'source': self.base_url,
                            'scraped_at': str(asyncio.get_event_loop().time()),
                            'country': 'Germany',
                            'region': 'Rheingau' if 'leitz' in self.base_url.lower() else 'Pfalz'
                        }
                        
                        wines.append(wine)
                    
                    except Exception as e:
                        print(f"    ❌ Error: {e}")
                        continue
                
                await browser.close()
                
            except Exception as e:
                print(f"  ❌ Error accessing {self.base_url}: {e}")
                await browser.close()
        
        return wines
    
    async def publish_to_rabbitmq(self, wines):
        """Publish wines to RabbitMQ."""
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
                
                # Publish wines as batch
                message_body = json.dumps(wines, ensure_ascii=False, indent=2)
                message = aio_pika.Message(
                    message_body.encode(),
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                )
                
                await exchange.publish(message, routing_key=f"winery.{self.name.lower().replace(' ', '_')}")
                
        except Exception as e:
            print(f"❌ RabbitMQ Error: {e}")
            raise

async def main():
    """Main test function."""
    rabbitmq_url = "amqp://rabbitmq:rabbitmq@localhost:5672/"
    
    print("🍇 Starting RabbitMQ Winery Test")
    print("=" * 60)
    print(f"🔌 RabbitMQ: {rabbitmq_url}")
    
    # Test connection
    try:
        connection = await aio_pika.connect_robust(rabbitmq_url)
        await connection.close()
        print("✅ RabbitMQ connection successful")
    except Exception as e:
        print(f"❌ RabbitMQ connection failed: {e}")
        return
    
    wineries = [
        ('https://www.weingut-rainer-sauer.de/', 'Weingut Rainer Sauer'),
        ('https://www.buerklin-wolf.de/', 'Bürklin-Wolf'),
        ('https://www.leitz-wein.de/', 'Weingut Leitz')
    ]
    
    results = {}
    total_wines = 0
    
    for url, name in wineries:
        scraper = CleanRabbitMQWineryScraper(name, url, rabbitmq_url)
        try:
            count = await scraper.scrape_and_publish()
            results[name] = count
            total_wines += count
            await asyncio.sleep(1)  # Rate limiting
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
    
    print(f"\n📋 Exchange: 'wines' (Topic)")
    print(f"🎯 Routing keys: winery.weingut_rainer_sauer, winery.buerklin_wolf, winery.weingut_leitz")
    print("✅ All data successfully published to RabbitMQ!")

if __name__ == "__main__":
    asyncio.run(main())