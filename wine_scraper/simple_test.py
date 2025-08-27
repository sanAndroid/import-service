#!/usr/bin/env python3
"""Simple test script for winery scraping without relative imports."""

import sys
import os
import asyncio

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules directly
from scrapers.winery import WineryScraper
from pipelines.models import Wine

async def test_winery():
    """Test scraping Weingut Rainer Sauer."""
    print("🍷 Testing winery scraping...")
    print("=" * 50)
    
    try:
        scraper = WineryScraper("Weingut Rainer Sauer", "https://www.weingut-rainer-sauer.de/")
        
        async with scraper:
            wines = await scraper.scrape_winery_site()
            
        print(f"✅ Successfully scraped {len(wines)} wines")
        
        # Show first few wines
        for i, wine in enumerate(wines[:3], 1):
            print(f"\n{i}. {wine.name}")
            print(f"   Winery: {wine.winery}")
            print(f"   Price: ${wine.price}" if wine.price else "   Price: N/A")
            print(f"   Vintage: {wine.vintage}" if wine.vintage else "   Vintage: N/A")
            print(f"   Type: {wine.type}" if wine.type else "   Type: N/A")
            print(f"   Region: {wine.region}" if wine.region else "   Region: N/A")
            print(f"   URL: {wine.shop_url}")
            
        print(f"\n📊 Total wines found: {len(wines)}")
        
        return wines
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    wines = asyncio.run(test_winery())