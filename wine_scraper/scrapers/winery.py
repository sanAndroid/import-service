"""Winery website scraper for direct winery scraping."""

import asyncio
import re
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.base import BaseScraper
from pipelines.models import Wine
from utils.observability import get_logger

logger = get_logger("scraper.winery")


class WineryScraper(BaseScraper):
    """Scraper for individual winery websites."""
    
    def __init__(self, winery_name: str, base_url: str):
        super().__init__(f"winery_{winery_name}", base_url)
        self.winery_name = winery_name
        self.base_url = base_url
    
    async def search(self, query: str = None) -> List[Wine]:
        """Search for wines on the winery website."""
        return await self.scrape_winery_site()
    
    async def get_wine_details(self, wine_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific wine."""
        # wine_id is the wine URL in this case
        return await self.extract_wine_details(wine_id)
    
    async def scrape_winery_site(self) -> List[Wine]:
        """Main method to scrape all wines from a winery website."""
        wines = []
        
        try:
            # First, try to find wine shop pages
            wine_urls = await self.discover_wine_urls()
            
            for wine_url in wine_urls:
                try:
                    wine_data = await self.extract_wine_details(wine_url)
                    if wine_data:
                        wine = self.create_wine_model(wine_data)
                        wines.append(wine)
                except Exception as e:
                    logger.error(f"Error extracting wine details from {wine_url}: {e}")
                    continue
            
            logger.info(f"Scraped {len(wines)} wines from {self.winery_name}")
            return wines
            
        except Exception as e:
            logger.error(f"Error scraping winery {self.winery_name}: {e}")
            return []
    
    async def discover_wine_urls(self) -> List[str]:
        """Discover wine product URLs on the winery website."""
        wine_urls = []
        
        # Common wine shop paths to check
        shop_paths = [
            "/shop",
            "/wines",
            "/products",
            "/store",
            "/shop/wines",
            "/wine-shop",
            "/weinshop",
            "/weine"
        ]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Try to find wine URLs from shop pages
                for shop_path in shop_paths:
                    shop_url = urljoin(self.base_url, shop_path)
                    try:
                        await page.goto(shop_url, wait_until="networkidle", timeout=30000)
                        
                        # Look for wine product links
                        wine_links = await self.extract_wine_links_from_page(page)
                        wine_urls.extend(wine_links)
                        
                        if wine_links:  # Found some wines, no need to try other paths
                            break
                            
                    except Exception:
                        continue
                
                # If no shop found, try crawling main site
                if not wine_urls:
                    wine_urls = await self.crawl_for_wine_urls(page, self.base_url)
                
            finally:
                await browser.close()
        
        # Remove duplicates and filter valid URLs
        wine_urls = list(set(wine_urls))
        wine_urls = [url for url in wine_urls if self.is_wine_url(url)]
        
        logger.info(f"Discovered {len(wine_urls)} wine URLs")
        return wine_urls
    
    async def extract_wine_links_from_page(self, page: Page) -> List[str]:
        """Extract wine product links from a page."""
        links = []
        
        # Common selectors for wine product links
        selectors = [
            "a[href*='wine']",
            "a[href*='product']",
            "a[href*='bottle']",
            ".wine-item a",
            ".product-item a",
            "[class*='wine'] a",
            "[class*='product'] a",
            "a[class*='wine']",
            "a[class*='product']"
        ]
        
        for selector in selectors:
            try:
                elements = await page.query_selector_all(selector)
                for element in elements:
                    href = await element.get_attribute('href')
                    if href:
                        full_url = urljoin(self.base_url, href)
                        links.append(full_url)
            except Exception:
                continue
        
        return links
    
    async def crawl_for_wine_urls(self, page: Page, start_url: str, max_depth: int = 2) -> List[str]:
        """Crawl website to discover wine URLs."""
        visited = set()
        wine_urls = []
        to_visit = [(start_url, 0)]
        
        while to_visit and len(wine_urls) < 50:  # Limit to prevent infinite crawling
            url, depth = to_visit.pop(0)
            
            if url in visited or depth > max_depth:
                continue
            
            visited.add(url)
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=10000)
                
                # Check if this is a wine product page
                if self.is_wine_url(url):
                    wine_urls.append(url)
                
                # Find more links to crawl
                if depth < max_depth:
                    links = await page.query_selector_all("a[href]")
                    for link in links:
                        href = await link.get_attribute('href')
                        if href:
                            full_url = urljoin(self.base_url, href)
                            if self.is_same_domain(full_url) and full_url not in visited:
                                to_visit.append((full_url, depth + 1))
                
            except Exception:
                continue
        
        return wine_urls
    
    def is_wine_url(self, url: str) -> bool:
        """Check if URL likely points to a wine product page."""
        url_lower = url.lower()
        wine_patterns = [
            r'wine',
            r'bottle',
            r'vin',
            r'wein',
            r'product',
            r'\d{4}',  # Vintage year
            r'cabernet|merlot|chardonnay|riesling|pinot|shiraz'  # Common grape varieties
        ]
        
        return any(re.search(pattern, url_lower) for pattern in wine_patterns)
    
    def is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain as the winery."""
        return urlparse(url).netloc == urlparse(self.base_url).netloc
    
    async def extract_wine_details(self, wine_url: str) -> Optional[Dict[str, Any]]:
        """Extract detailed information from a wine product page."""
        try:
            html = await self.fetch_with_playwright(wine_url)
            soup = self.parse_html(html)
            
            # Extract all available wine information
            wine_data = {
                'name': self.extract_wine_name(soup, wine_url),
                'winery': self.winery_name,
                'url': wine_url,
                'price': self.extract_price(soup),
                'description': self.extract_description(soup),
                'vintage': self.extract_vintage(soup),
                'grapes': self.extract_grape_varieties(soup),
                'region': self.extract_region(soup),
                'country': self.extract_country(soup),
                'type': self.extract_wine_type(soup),
                'alcohol_content': self.extract_alcohol_content(soup),
                'image_url': self.extract_image_url(soup, wine_url),
                'quality_level': self.extract_quality_level(soup),
                'bottle_size': self.extract_bottle_size(soup),
                'average_rating': self.extract_average_rating(soup),
                'number_of_ratings': self.extract_number_of_ratings(soup),
                'critic_scores': self.extract_critic_scores(soup),
                'food_pairings': self.extract_food_pairings(soup),
                'serving_temperature': self.extract_serving_temperature(soup),
                'availability_status': self.extract_availability_status(soup),
                'sku': self.extract_sku(soup)
            }
            
            # Filter out None values
            wine_data = {k: v for k, v in wine_data.items() if v is not None}
            
            logger.debug(f"Extracted wine data: {wine_data}")
            return wine_data
            
        except Exception as e:
            logger.error(f"Error extracting wine details from {wine_url}: {e}")
            return None
    
    def extract_wine_name(self, soup: BeautifulSoup, url: str) -> Optional[str]:
        """Extract wine name from page."""
        selectors = [
            "h1",
            ".product-title",
            ".wine-name",
            "[class*='wine-title']",
            "[class*='product-name']",
            "meta[property='og:title']"
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if selector == "meta[property='og:title']":
                    return element.get('content', '').strip()
                return element.get_text(strip=True)
        
        # Fallback to URL
        return url.split('/')[-1].replace('-', ' ').replace('_', ' ').title()
    
    def extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract wine price."""
        price_selectors = [
            ".price",
            ".product-price",
            "[class*='price']",
            "meta[property='product:price:amount']"
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text() if hasattr(element, 'get_text') else str(element)
                if text:
                    # Extract number from price text
                    price_match = re.search(r'[\d,.]+', text.replace(',', ''))
                    if price_match:
                        try:
                            return float(price_match.group())
                        except ValueError:
                            continue
        
        return None
    
    def extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract wine description."""
        description_selectors = [
            ".description",
            ".product-description",
            "[class*='description']",
            "meta[property='og:description']",
            ".wine-notes",
            ".tasting-notes"
        ]
        
        for selector in description_selectors:
            element = soup.select_one(selector)
            if element:
                if selector == "meta[property='og:description']":
                    return element.get('content', '').strip()
                return element.get_text(strip=True)
        
        return None
    
    def extract_vintage(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract vintage year."""
        text = soup.get_text()
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        if year_match:
            try:
                return int(year_match.group())
            except ValueError:
                pass
        return None
    
    def extract_grape_varieties(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """Extract grape varieties."""
        grape_selectors = [
            ".grape",
            ".varietal",
            ".grape-variety",
            "[class*='grape']",
            "[class*='varietal']"
        ]
        
        for selector in grape_selectors:
            elements = soup.select(selector)
            if elements:
                varieties = []
                for element in elements:
                    text = element.get_text(strip=True)
                    if text:
                        varieties.extend([v.strip() for v in text.split(',')])
                return varieties
        
        return None
    
    def extract_region(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract wine region."""
        region_selectors = [
            ".region",
            ".wine-region",
            "[class*='region']",
            ".origin"
        ]
        
        for selector in region_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return None
    
    def extract_country(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract country of origin."""
        country_selectors = [
            ".country",
            ".origin-country",
            "[class*='country']"
        ]
        
        for selector in country_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return None
    
    def extract_wine_type(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract wine type (red, white, etc.)."""
        type_selectors = [
            ".wine-type",
            ".type",
            "[class*='type']"
        ]
        
        for selector in type_selectors:
            element = soup.select_one(selector)
            if element:
                wine_type = element.get_text(strip=True).lower()
                if any(t in wine_type for t in ['red', 'white', 'rosé', 'sparkling', 'dessert']):
                    return wine_type.title()
        
        # Try to infer from description
        description = self.extract_description(soup)
        if description:
            description_lower = description.lower()
            if 'red' in description_lower:
                return "Red"
            elif 'white' in description_lower:
                return "White"
            elif 'rosé' in description_lower or 'rose' in description_lower:
                return "Rosé"
            elif 'sparkling' in description_lower or 'champagne' in description_lower:
                return "Sparkling"
        
        return None
    
    def extract_alcohol_content(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract alcohol content percentage."""
        text = soup.get_text()
        alcohol_match = re.search(r'(\d+(?:\.\d+)?)%\s*alcohol', text, re.IGNORECASE)
        if not alcohol_match:
            alcohol_match = re.search(r'(\d+(?:\.\d+)?)%\s*vol', text, re.IGNORECASE)
        
        if alcohol_match:
            try:
                return float(alcohol_match.group(1))
            except ValueError:
                pass
        
        return None
    
    def extract_image_url(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract wine image URL."""
        image_selectors = [
            ".product-image img",
            ".wine-image img",
            "img[src*='wine']",
            "meta[property='og:image']"
        ]
        
        for selector in image_selectors:
            element = soup.select_one(selector)
            if element:
                if selector == "meta[property='og:image']":
                    src = element.get('content')
                else:
                    src = element.get('src')
                
                if src:
                    return urljoin(base_url, src)
        
        return None
    
    def extract_quality_level(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract quality level indicators."""
        text = soup.get_text()
        quality_indicators = [
            "Großes Gewächs",
            "Grand Cru",
            "Ortswein",
            "Gutswein",
            "Premier Cru",
            "Classico",
            "Riserva",
            "Gran Riserva"
        ]
        
        for indicator in quality_indicators:
            if indicator.lower() in text.lower():
                return indicator
        
        return None
    
    def extract_bottle_size(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract bottle size."""
        text = soup.get_text()
        size_match = re.search(r'(\d+(?:\.\d+)?)\s*(ml|l|cl)', text, re.IGNORECASE)
        if size_match:
            return f"{size_match.group(1)}{size_match.group(2).upper()}"
        
        return "750ml"  # Default
    
    def extract_average_rating(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract average rating."""
        rating_selectors = [
            ".rating",
            ".average-rating",
            "[class*='rating']"
        ]
        
        for selector in rating_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text()
                rating_match = re.search(r'(\d+(?:\.\d+)?)', text)
                if rating_match:
                    try:
                        rating = float(rating_match.group(1))
                        if 0 <= rating <= 100:
                            return rating / 10 if rating > 10 else rating
                    except ValueError:
                        continue
        
        return None
    
    def extract_number_of_ratings(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract number of ratings."""
        text = soup.get_text()
        rating_count_match = re.search(r'(\d+)\s*ratings?', text, re.IGNORECASE)
        if not rating_count_match:
            rating_count_match = re.search(r'(\d+)\s*reviews?', text, re.IGNORECASE)
        
        if rating_count_match:
            try:
                return int(rating_count_match.group(1))
            except ValueError:
                pass
        
        return None
    
    def extract_critic_scores(self, soup: BeautifulSoup) -> Optional[Dict[str, float]]:
        """Extract critic scores."""
        # This is complex and would need specific selectors for each winery
        return None
    
    def extract_food_pairings(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """Extract food pairing recommendations."""
        pairing_selectors = [
            ".food-pairing",
            ".pairing",
            "[class*='pairing']",
            ".serving-suggestions"
        ]
        
        for selector in pairing_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text()
                foods = re.split(r'[,\n]+', text)
                return [food.strip() for food in foods if food.strip()]
        
        return None
    
    def extract_serving_temperature(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract serving temperature."""
        temp_selectors = [
            ".serving-temperature",
            ".temperature",
            "[class*='temp']"
        ]
        
        for selector in temp_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return None
    
    def extract_availability_status(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract availability status."""
        availability_selectors = [
            ".availability",
            ".stock",
            ".in-stock",
            ".out-of-stock"
        ]
        
        for selector in availability_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True).lower()
                if 'out' in text or 'unavailable' in text:
                    return "Out of Stock"
                elif 'in' in text or 'available' in text:
                    return "In Stock"
                else:
                    return text.title()
        
        return None
    
    def extract_sku(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract SKU/Product ID."""
        sku_selectors = [
            ".sku",
            ".product-id",
            ".item-id",
            "[data-sku]",
            "[class*='sku']"
        ]
        
        for selector in sku_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True) or element.get('data-sku')
        
        return None
    
    def create_wine_model(self, wine_data: Dict[str, Any]) -> Wine:
        """Create Wine model from extracted data."""
        return Wine(
            name=wine_data.get('name', 'Unknown Wine'),
            winery=wine_data.get('winery', self.winery_name),
            winery_website=self.base_url,
            type=wine_data.get('type'),
            region=wine_data.get('region'),
            country=wine_data.get('country'),
            grapes=wine_data.get('grapes'),
            alcohol_content=wine_data.get('alcohol_content'),
            vintage=wine_data.get('vintage'),
            price=wine_data.get('price'),
            description=wine_data.get('description'),
            image_url=wine_data.get('image_url'),
            quality_level=wine_data.get('quality_level'),
            shop_url=wine_data.get('url'),
            bottle_size=wine_data.get('bottle_size'),
            average_rating=wine_data.get('average_rating'),
            number_of_ratings=wine_data.get('number_of_ratings'),
            critic_scores=wine_data.get('critic_scores'),
            food_pairings=wine_data.get('food_pairings'),
            serving_temperature=wine_data.get('serving_temperature'),
            availability_status=wine_data.get('availability_status'),
            sku=wine_data.get('sku'),
            source_urls=[wine_data.get('url', '')]
        )