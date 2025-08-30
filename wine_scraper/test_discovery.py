import asyncio
from urllib.parse import urlparse
from scrapers.winery import WineryScraper

async def main():
    wineries = [
        {"name": "Weingut Johannishof", "url": "https://www.weingut-johannishof.de/"},
    ]

    for winery in wineries:
        print(f"--- Starting discovery for {winery['name']} ---")
        scraper = WineryScraper(winery_name=winery['name'], base_url=winery['url'])
        
        try:
            wine_urls = await scraper.discover_wine_urls()
            
            # Generate a filename from the winery name
            parsed_url = urlparse(winery['url'])
            domain = parsed_url.netloc.replace('www.', '')
            filename = f"{domain}_urls.txt"
            
            with open(filename, 'w') as f:
                for url in wine_urls:
                    f.write(f"{url}\n")
            
            print(f"✅ Found {len(wine_urls)} URLs. Saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error scraping {winery['name']}: {e}")
        
        print("-" * (len(winery['name']) + 24))
        print() # Add a blank line for readability

if __name__ == "__main__":
    asyncio.run(main())
