#!/usr/bin/env python3
"""Direct test for winery scraping without import issues."""

import sys
import os
import asyncio
import re
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any, Optional

from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

# Simple wine data class for testing
class SimpleWine:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class SimpleWineryScraper:
    """Simplified winery scraper for testing."""
    
    def __init__(self, winery_name: str, base_url: str):
        self.winery_name = winery_name
        self.base_url = base_url
    
    async def scrape_winery_site(self) -> List[Dict[str, Any]]:
        """Main method to scrape all wines from a winery website."""
        wines = []
        
        try:
            wine_urls = await self.discover_wine_urls()
            print(f"🔗 Found {len(wine_urls)} wine URLs to process")
            
            for wine_url in wine_urls[:5]:  # Limit to first 5 for testing
                try:
                    wine_data = await self.extract_wine_details(wine_url)
                    if wine_data and wine_data.get('name'):
                        wines.append(wine_data)
                        print(f"✅ Scraped: {wine_data.get('name', 'Unknown')}")
                except Exception as e:
                    print(f"⚠️  Error extracting from {wine_url}: {e}")
                    continue
            
            print(f"🍷 Total wines scraped: {len(wines)}")
            return wines
            
        except Exception as e:
            print(f"❌ Error scraping winery: {e}")
            return []
    
    async def discover_wine_urls(self) -> List[str]:
        """Discover wine URLs on the winery website."""
        wine_urls = []
        shop_paths = ["/shop", "/wines", "/products", "/store"]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                for shop_path in shop_paths:
                    shop_url = urljoin(self.base_url, shop_path)
                    try:
                        print(f"🌐 Checking: {shop_url}")
                        await page.goto(shop_url, wait_until="networkidle", timeout=10000)
                        
                        # Look for wine links
                        links = await page.query_selector_all("a[href*='wine'], a[href*='product'], .wine-item a, .product-item a")
                        for link in links:
                            href = await link.get_attribute('href')
                            if href:
                                full_url = urljoin(self.base_url, href)
                                if self.is_wine_url(full_url):
                                    wine_urls.append(full_url)
                        
                        if wine_urls:
                            break
                            
                    except Exception:
                        continue
                
                # Also check main page
                if not wine_urls:
                    await page.goto(self.base_url, wait_until="networkidle", timeout=10000)
                    links = await page.query_selector_all("a[href*='/wine'], a[href*='/product']")
                    for link in links:
                        href = await link.get_attribute('href')
                        if href:
                            full_url = urljoin(self.base_url, href)
                            if self.is_wine_url(full_url):
                                wine_urls.append(full_url)
                
            finally:
                await browser.close()
        
        return list(set(wine_urls))
    
    def is_wine_url(self, url: str) -> bool:
        """Check if URL likely points to a wine product page."""
        url_lower = url.lower()
        wine_patterns = [r'wine', r'product', r'bottle', r'\d{4}']
        return any(re.search(pattern, url_lower) for pattern in wine_patterns)
    
    async def extract_wine_details(self, wine_url: str) -> Optional[Dict[str, Any]]:
        """Extract detailed information from a wine product page."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                await page.goto(wine_url, wait_until="networkidle", timeout=10000)
                html = await page.content()
                await browser.close()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract basic wine information
            wine_data = {
                'name': self.extract_text(soup, ['h1', '.product-title', '.wine-name']),
                'winery': self.winery_name,
                'url': wine_url,
                'price': self.extract_price(soup),
                'description': self.extract_text(soup, ['.description', '.product-description']),
                'vintage': self.extract_vintage(soup),
                'type': self.extract_wine_type(soup),
                'region': self.extract_text(soup, ['.region', '.wine-region']),
            }
            
            # Clean up None values
            return {k: v for k, v in wine_data.items() if v is not None}
            
        except Exception as e:
            print(f"⚠️  Error loading {wine_url}: {e}")
            return None
    
    def extract_text(self, soup, selectors):
        """Extract text using CSS selectors."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def extract_price(self, soup):
        """Extract price from page."""
        text = soup.get_text()
        price_match = re.search(r'€\s*(\d+(?:\.\d+)?(?:,\d+)?)', text)
        if not price_match:
            price_match = re.search(r'\$(\d+(?:\.\d+)?)', text)
        if not price_match:
            price_match = re.search(r'(\d+(?:\.\d+)?)\s*€', text)
        
        if price_match:
            price_str = price_match.group(1).replace(',', '.')
            try:
                return float(price_str)
            except ValueError:
                pass
        return None
    
    def extract_vintage(self, soup):
        """Extract vintage year."""
        text = soup.get_text()
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        if year_match:
            try:
                year = int(year_match.group())
                if 1900 <= year <= 2030:
                    return year
            except ValueError:
                pass
        return None
    
    def extract_wine_type(self, soup):
        """Extract wine type."""
        text = soup.get_text().lower()
        if 'red' in text:
            return "Red"
        elif 'white' in text:
            return "White"
        elif 'rosé' in text or 'rose' in text:
            return "Rosé"
        elif 'sparkling' in text:
            return "Sparkling"
        return None

async def main():
    """Main test function."""
    print("🍷 Wine Scraper - Single Winery Test")
    print("=" * 40)
    
    winery_name = "Bürklin-Wolf"
    winery_url = "https://shop.buerklin-wolf.de/"
    
    scraper = SimpleWineryScraper(winery_name, winery_url)
    wines = await scraper.scrape_winery_site()
    
    if wines:
        print("\n🍾 Sample wines found:")
        for i, wine in enumerate(wines[:3], 1):
            print(f"\n{i}. {wine.get('name', 'N/A')}")
            print(f"   Price: €{wine.get('price', 'N/A')}")
            print(f"   Vintage: {wine.get('vintage', 'N/A')}")
            print(f"   Type: {wine.get('type', 'N/A')}")
            print(f"   URL: {wine.get('url', 'N/A')}")
    else:
        print("\n❌ No wines found")

if __name__ == "__main__":
    asyncio.run(main())