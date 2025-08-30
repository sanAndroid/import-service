import asyncio
from scrapers.winery import WineryScraper

async def main():
    scraper = WineryScraper("test", "https://www.adeneuer.de/")
    async with scraper:
        wines = await scraper.scrape_winery_site()
        print(wines)

if __name__ == "__main__":
    asyncio.run(main())