#!/usr/bin/env python3
"""Improved test for winery scraping with better detection."""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class ImprovedWineryScraper:
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url
    
    async def scrape_winery_site(self):
        """Improved scraping with better wine detection."""
        wines = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                print(f"  Loading {self.base_url}...")
                await page.goto(self.base_url, wait_until="domcontentloaded", timeout=45000)
                
                # Wait a bit for dynamic content
                await asyncio.sleep(2)
                
                # Look for wine-related links more specifically
                wine_selectors = [
                    "a[href*='wein']",
                    "a[href*='wine']", 
                    "a[href*='produkt']",
                    "a[href*='shop']",
                    "a[href*='sortiment']",
                    "a[href*='riesling']",
                    "a[href*='silvaner']",
                    "a[href*='spatburgunder']",
                    "a[href*='weissburgunder']",
                    ".wine-item a",
                    ".product-item a",
                    ".shop-item a"
                ]
                
                wine_urls = []
                
                for selector in wine_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        for element in elements:
                            href = await element.get_attribute('href')
                            text = await element.inner_text()
                            
                            if href and not href.startswith('mailto:'):
                                full_url = urljoin(self.base_url, href)
                                
                                # Better wine detection
                                text_lower = text.lower()
                                href_lower = href.lower()
                                
                                wine_keywords = ['riesling', 'silvaner', 'spätburgunder', 'weissburgunder', 
                                               'grauer burgunder', 'pinot', 'chasselas', 'cabernet', 'wein', 'wine']
                                
                                if any(keyword in text_lower or keyword in href_lower for keyword in wine_keywords):
                                    if full_url not in wine_urls and len(full_url) > 20:
                                        wine_urls.append(full_url)
                    except:
                        continue
                
                print(f"  Found {len(wine_urls)} wine-related URLs")
                
                # Also check main page for shop links
                try:
                    shop_links = await page.query_selector_all("a[href*='shop'], a[href*='sortiment'], a[href*='weine']")
                    for link in shop_links:
                        href = await link.get_attribute('href')
                        if href and 'shop' in href.lower() or 'sortiment' in href.lower() or 'weine' in href.lower():
                            full_url = urljoin(self.base_url, href)
                            if full_url not in wine_urls and full_url != self.base_url:
                                wine_urls.append(full_url)
                except:
                    pass
                
                # Remove duplicates and filter
                wine_urls = list(set(wine_urls))[:8]
                
                print(f"  Processing {len(wine_urls)} wine URLs...")
                
                # Extract wine data
                for wine_url in wine_urls:
                    try:
                        print(f"    Checking: {wine_url}")
                        await page.goto(wine_url, wait_until="domcontentloaded", timeout=15000)
                        await asyncio.sleep(1)
                        
                        content = await page.content()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Get page title
                        title = soup.find('h1')
                        if not title:
                            title = soup.find('title')
                        
                        name = "Unknown Wine"
                        if title:
                            name = title.get_text().strip()
                            # Clean up common suffixes
                            for suffix in [' | Weingut', ' - Weingut', ' | Weine', ' - Shop']:
                                if suffix in name:
                                    name = name.split(suffix)[0].strip()
                        
                        # Look for price
                        price = None
                        price_selectors = [
                            '.price',
                            '.product-price',
                            '.current-price',
                            '[class*="price"]',
                            'meta[property="product:price:amount"]'
                        ]
                        
                        for selector in price_selectors:
                            element = soup.select_one(selector)
                            if element:
                                if selector == 'meta[property="product:price:amount"]':
                                    price_text = element.get('content', '')
                                else:
                                    price_text = element.get_text()
                                
                                price_match = re.search(r'(\d+(?:[.,]\d+)?)', price_text)
                                if price_match:
                                    price = float(price_match.group(1).replace(',', '.'))
                                    break
                        
                        # Look for vintage
                        vintage = None
                        text = soup.get_text()
                        year_match = re.search(r'\b(20[0-2][0-9]|19[5-9][0-9])\b', text)
                        if year_match:
                            year = int(year_match.group(1))
                            if 1950 <= year <= 2025:
                                vintage = year
                        
                        # Skip if it looks like a category page
                        if 'weine' in name.lower() or 'shop' in name.lower() or 'sortiment' in name.lower():
                            continue
                        
                        wine_data = {
                            'name': name,
                            'winery': self.name,
                            'price': price,
                            'vintage': vintage,
                            'url': wine_url
                        }
                        
                        if len(name) > 5 and name.lower() != 'weine':
                            wines.append(wine_data)
                    
                    except Exception as e:
                        print(f"    Error: {e}")
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
    
    scraper = ImprovedWineryScraper(name, url)
    try:
        wines = await scraper.scrape_winery_site()
        print(f"✅ SUCCESS: Found {len(wines)} wines")
        
        for i, wine in enumerate(wines[:5], 1):
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
    
    print("🍇 Starting Improved Winery Scraping Test")
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


if __name__ == "__main__":
    asyncio.run(main())