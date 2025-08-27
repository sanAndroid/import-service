#!/usr/bin/env python3
"""Demo script for single winery scraping with working example."""

import asyncio
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_buerklin_wolf():
    """Scrape Bürklin-Wolf wines from their shop."""
    
    print("🍷 Demo: Scraping Bürklin-Wolf Winery")
    print("=" * 50)
    
    shop_url = "https://shop.buerklin-wolf.de/"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("🔗 Loading shop...")
            await page.goto(shop_url, wait_until="domcontentloaded", timeout=30000)
            
            # Get all product links
            links = await page.query_selector_all('a')
            
            wines = []
            for link in links:
                href = await link.get_attribute('href')
                text = await link.text_content()
                
                if href and text:
                    href = href.strip()
                    text = text.strip()
                    
                    # Look for wine product links
                    if href.endswith('.html') and len(text) > 3 and not text.startswith('http'):
                        wine_url = href if href.startswith('http') else f"https://shop.buerklin-wolf.de{href}"
                        
                        # Basic wine info
                        wine = {
                            'name': text,
                            'winery': 'Bürklin-Wolf',
                            'url': wine_url,
                            'price': None,
                            'type': None,
                            'vintage': None
                        }
                        wines.append(wine)
            
            print(f"✅ Found {len(wines)} wine categories/products")
            
            # Show first few wines
            for i, wine in enumerate(wines[:5], 1):
                print(f"\n{i}. {wine['name']}")
                print(f"   URL: {wine['url']}")
                
            # Try to get details from a specific wine page
            if wines:
                sample_wine = wines[0]
                print(f"\n📋 Getting details for: {sample_wine['name']}")
                
                try:
                    await page.goto(sample_wine['url'], wait_until="domcontentloaded", timeout=15000)
                    
                    # Extract more details
                    title = await page.title()
                    print(f"   Page Title: {title}")
                    
                    # Look for price
                    price_elements = await page.query_selector_all('*[class*="price"], .price')
                    for price_el in price_elements:
                        price_text = await price_el.text_content()
                        if price_text and '€' in price_text:
                            print(f"   Price: {price_text.strip()}")
                            break
                    
                except Exception as e:
                    print(f"   ⚠️  Could not load details: {e}")
            
            return wines
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
        finally:
            await browser.close()

if __name__ == "__main__":
    wines = asyncio.run(scrape_buerklin_wolf())
    
    if wines:
        print(f"\n🎉 Successfully scraped {len(wines)} wine items!")
        print("\n📊 Summary:")
        for wine in wines[:3]:
            print(f"   • {wine['name']} - {wine['url']}")
    else:
        print("\n❌ No wines found")