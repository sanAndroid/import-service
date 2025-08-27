#!/usr/bin/env python3
"""Simple test script for winery scraping."""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import directly
from scrapers.winery import WineryScraper

# Mock settings to avoid import issues
class MockSettings:
    http_retries = 3
    rate_limit_delay = 1
    playwright_headless = True
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ]
    cache_ttl = 3600
    output_dir = "./data"

# Monkey patch settings
import scrapers.base as base_module
base_module.settings = MockSettings()

async def test_winery(url: str, name: str):
    """Test scraping for a single winery."""
    print(f"\n🍷 Testing {name}")
    print(f"URL: {url}")
    print("-" * 50)
    
    scraper = WineryScraper(name, url)
    try:
        async with scraper:
            wines = await scraper.scrape_winery_site()
            
            print(f"✅ SUCCESS: Found {len(wines)} wines")
            
            # Show first 3 wines
            for i, wine in enumerate(wines[:3], 1):
                print(f"  {i}. {wine.name}")
                print(f"     Price: €{wine.price or 'N/A'}")
                print(f"     Vintage: {wine.vintage or 'N/A'}")
                print(f"     Type: {wine.type or 'N/A'}")
                print()
            
            return len(wines)
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 0

async def main():
    """Run tests on all three wineries."""
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