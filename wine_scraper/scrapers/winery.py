"""Winery website scraper for direct winery scraping."""

import asyncio
from typing import List, Dict, Any, Optional

from playwright.async_api import async_playwright

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.base import BaseScraper
from scrapers.discovery import UrlDiscoverer
from scrapers.extractor import WineDataExtractor
from config.settings import settings
from pipelines.models import Wine
from utils.observability import get_logger

logger = get_logger("scraper.winery")


class WineryScraper(BaseScraper):
    """
    Orchestrates the scraping of a winery website by using separate services
    for URL discovery and data extraction.
    """
    
    def __init__(self, winery_name: str, base_url: str):
        super().__init__(f"winery_{winery_name}", base_url)
        self.winery_name = winery_name
        if base_url.startswith("http://"):
            self.base_url = base_url.replace("http://", "https://")
        else:
            self.base_url = base_url
    
    async def search(self, query: str = None) -> List[Wine]:
        """Search for wines on the winery website."""
        return await self.scrape_winery_site()
    
    async def get_wine_details(self, wine_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific wine."""
        # wine_id is the wine URL in this case
        return await self.extract_wine_details(wine_id)
    
    async def discover_wine_urls(self) -> List[str]:
        """
        Discovers wine product URLs using the UrlDiscoverer service.
        """
        async with async_playwright() as p:
            browser = None
            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()
                page.set_default_timeout(settings.scraper_default_timeout)
                
                discoverer = UrlDiscoverer(page, self.base_url)
                wine_urls = await discoverer.discover_wine_urls()
                
                logger.info(f"Discovered {len(wine_urls)} wine URLs")
                return wine_urls
            finally:
                if browser:
                    await browser.close()

    async def scrape_winery_site(self) -> List[Wine]:
        """Main method to scrape all wines from a winery website."""
        wines = []
        
        try:
            wine_urls = await self.discover_wine_urls()
            
            for wine_url in wine_urls:
                logger.info(f"Processing wine URL: {wine_url}")
                try:
                    wine_data = await self.extract_wine_details(wine_url)
                    if wine_data:
                        wine = self.create_wine_model(wine_data)
                        if wine:
                            wines.append(wine)
                except Exception as e:
                    logger.error(f"Error extracting wine details from {wine_url}: {e}")
                    continue
            
            logger.info(f"Scraped {len(wines)} wines from {self.winery_name}")
            return wines
            
        except Exception as e:
            logger.error(f"Error scraping winery {self.winery_name}: {e}")
            return []

    async def extract_wine_details(self, wine_url: str) -> Optional[Dict[str, Any]]:
        """
        Fetches a wine page and uses the WineDataExtractor to get structured data.
        """
        try:
            html = await self.fetch_with_playwright(wine_url)
            soup = self.parse_html(html)
            
            extractor = WineDataExtractor(soup, wine_url)
            wine_data = {}
            try:
                wine_data = extractor.extract_all()
            except ValueError as e:
                logger.warning(f"ValueError during extraction from {wine_url}: {e}")

            # Add data that the extractor doesn't know about
            wine_data['winery'] = self.winery_name
            wine_data['url'] = wine_url
            
            logger.debug(f"Extracted wine data: {wine_data}")
            return wine_data
            
        except Exception as e:
            logger.error(f"Error extracting wine details from {wine_url}: {e}")
            return None
    
    def create_wine_model(self, wine_data: Dict[str, Any]) -> Optional[Wine]:
        """Create Wine model from extracted data, returning None if it's not a valid wine page."""
        name = wine_data.get('name')
        price = wine_data.get('price')
        shop_url = wine_data.get('url')

        if not name or not price or not shop_url:
            return None

        # Filter out common non-product page titles
        if any(keyword in name.lower() for keyword in ['impressum', 'datenschutz', 'agb', 'versand', 'kontakt', 'about', 'blog', 'news', 'events', 'warenkorb', 'cart', 'kasse', 'checkout']):
            return None

        return Wine(
            name=name,
            winery_name=wine_data.get('winery', self.winery_name),
            winery_website=self.base_url,
            type=wine_data.get('type'),
            region=wine_data.get('region'),
            country=wine_data.get('country'),
            grapes=wine_data.get('grapes'),
            alcohol_content=wine_data.get('alcohol_content'),
            vintage=wine_data.get('vintage'),
            price=price,
            description=wine_data.get('description'),
            image_url=wine_data.get('image_url'),
            quality_level=wine_data.get('quality_level'),
            shop_url=shop_url,
            bottle_size=wine_data.get('bottle_size', '750ml'),
            average_rating=wine_data.get('average_rating'),
            number_of_ratings=wine_data.get('number_of_ratings'),
            critic_scores=wine_data.get('critic_scores', {}),
            food_pairings=wine_data.get('food_pairings'),
            serving_temperature=wine_data.get('serving_temperature'),
            availability_status=wine_data.get('availability_status'),
            sku=wine_data.get('sku'),
            source_urls=[shop_url]
        )