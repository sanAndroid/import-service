#!/usr/bin/env python3
"""Test script for winery scraping."""

import asyncio
import sys
from pathlib import Path

# Add the src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.winery import WineryScraper


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
            
            # Show first 5 wines
            for i, wine in enumerate(wines[:5], 1):
                print(f"  {i}. {wine.name}")
                print(f"     Price: €{wine.price or 'N/A'}")
                print(f"     Vintage: {wine.vintage or 'N/A'}")
                print(f"     Type: {wine.type or 'N/A'}")
                print(f"     Region: {wine.region or 'N/A'}")
                print()
            
            return len(wines)
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
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
    print(f"📈 SUCCESS RATE: {sum(1 for c in results.values() if c > 0)}/{len(wineries)} ({sum(1 for c in results.values() if c > 0)/len(wineries)*100:.0f}%)")


if __name__ == "__main__":
    asyncio.run(main())