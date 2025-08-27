#!/usr/bin/env python3
"""Test script for single winery scraping."""

import asyncio
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers.winery import WineryScraper

async def test_single_winery():
    """Test scraping a single winery."""
    winery_name = "Weingut Rainer Sauer"
    winery_url = "https://www.weingut-rainer-sauer.de/"
    
    print(f"🍷 Testing scraping for: {winery_name}")
    print(f"🔗 URL: {winery_url}")
    print()
    
    try:
        scraper = WineryScraper(winery_name, winery_url)
        
        async with scraper:
            wines = await scraper.scrape_winery_site()
            
        print(f"✅ Found {len(wines)} wines:")
        print()
        
        for i, wine in enumerate(wines[:5], 1):  # Show first 5 wines
            print(f"{i}. {wine.name}")
            print(f"   Price: ${wine.price}" if wine.price else "   Price: N/A")
            print(f"   Vintage: {wine.vintage}" if wine.vintage else "   Vintage: N/A")
            print(f"   Type: {wine.type}" if wine.type else "   Type: N/A")
            print()
            
        if len(wines) > 5:
            print(f"... and {len(wines) - 5} more wines")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    
    return wines

if __name__ == "__main__":
    wines = asyncio.run(test_single_winery())