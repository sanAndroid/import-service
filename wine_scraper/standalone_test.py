#!/usr/bin/env python3
"""Standalone test for winery scraping."""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class SimpleWineryScraper:
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url
    
    async def scrape_winery_site(self):
        """Simple scraping without complex imports."""
        wines = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                await page.goto(self.base_url, wait_until="networkidle", timeout=30000)
                
                # Get all links that might be wine products
                links = await page.query_selector_all("a[href]")
                wine_urls = []
                
                for link in links:
                    href = await link.get_attribute('href')
                    if href:
                        full_url = urljoin(self.base_url, href)
                        text = await link.inner_text()
                        
                        # Simple wine detection
                        text_lower = text.lower()
                        if any(word in text_lower for word in ['riesling', 'silvaner', 'spätburgunder', 'weissburgunder', 'grauer burgunder', 'wine', 'wein']):
                            if full_url not in wine_urls:
                                wine_urls.append(full_url)
                
                # Limit to first 10 wine URLs
                wine_urls = wine_urls[:10]
                print(f"Found {len(wine_urls)} potential wine URLs for {self.name}")
                
                # Extract basic info from each wine page
                for wine_url in wine_urls[:5]:  # Limit to 5 for testing
                    try:
                        await page.goto(wine_url, wait_until="networkidle", timeout=15000)
                        
                        # Get page content
                        content = await page.content()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Extract basic info
                        title = soup.find('title')
                        title_text = title.text.strip() if title else wine_url.split('/')[-1]
                        
                        # Look for price
                        price_text = None
                        for selector in ['.price', '[class*="price"]', 'meta[property="product:price:amount"]']:
                            element = soup.select_one(selector)
                            if element:
                                if selector == 'meta[property="product:price:amount"]':
                                    price_text = element.get('content')
                                else:
                                    price_text = element.get_text()
                                break
                        
                        # Extract price number
                        price = None
                        if price_text:
                            price_match = re.search(r'(\d+(?:[.,]\d+)?)', price_text)
                            if price_match:
                                price = float(price_match.group(1).replace(',', '.'))
                        
                        # Extract vintage
                        vintage = None
                        text = soup.get_text()
                        year_match = re.search(r'\b(20\d{2}|19\d{2})\b', text)
                        if year_match:
                            vintage = int(year_match.group(1))
                        
                        wine = {
                            'name': title_text.replace(' | Weingut Rainer Sauer', '').replace(' | Bürklin-Wolf', '').replace(' | Weingut Leitz', '').strip(),
                            'winery': self.name,
                            'price': price,
                            'vintage': vintage,
                            'url': wine_url
                        }
                        
                        if wine['name'] and len(wine['name']) > 3:  # Basic filter
                            wines.append(wine)
                    
                    except Exception as e:
                        print(f"  Error processing {wine_url}: {e}")
                        continue
                
                await browser.close()
                
            except Exception as e:
                print(f"Error accessing {self.base_url}: {e}")
                await browser.close()
        
        return wines

async def test_winery(url, name):
    print(f"\n🍷 Testing {name}")
    print(f"URL: {url}")
    print("-" * 50)
    
    scraper = SimpleWineryScraper(name, url)
    try:
        wines = await scraper.scrape_winery_site()
        print(f"✅ SUCCESS: Found {len(wines)} wines")
        
        for i, wine in enumerate(wines[:3], 1):
            print(f"  {i}. {wine['name']}")
            print(f"     Price: €{wine['price'] or 'N/A'}")
            print(f"     Vintage: {wine['vintage'] or 'N/A'}")
            print()
        
        return len(wines)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 0

async def main():
    wineries = [
        ('https://www.weingut-rainer-sauer.de/', 'Weingut Rainer Sauer'),
        ('https://www.buerklin-wolf.de/', 'Bürklin-Wolf'),
        ('https://www.leitz-wein.de/', 'Weingut Leitz')
    ]
    
    print("🍇 Starting Winery Scraping Test")
    print("=" * 60)
    
    results = {}
    total_wines = 0
    
    for url, name in wineries:
        count = await test_winery(url, name)
        results[name] = count
        total_wines += count
    
    print("\n📊 TEST SUMMARY")
    print("=" * 60)
    for name, count in results.items():
        status = "✅ SUCCESS" if count > 0 else "❌ FAILED"
        print(f"{name}: {count} wines - {status}")
    
    print(f"\n🎯 TOTAL: {total_wines} wines found across {len(wineries)} wineries")
    
    success_count = sum(1 for c in results.values() if c > 0)
    success_rate = (success_count / len(wineries)) * 100
    print(f"📈 SUCCESS RATE: {success_count}/{len(wineries)} ({success_rate:.0f}%)")

if __name__ == "__main__":
    asyncio.run(main())