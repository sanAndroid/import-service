"""Base scraper class with common functionality."""

import asyncio
import random
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from tenacity import retry, stop_after_attempt, wait_exponential

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import settings
from utils.http import create_http_client
from utils.cache import Cache
from utils.observability import get_logger


class BaseScraper(ABC):
    """Base class for all scrapers with common functionality."""

    def __init__(self, site_name: str, base_url: str):
        self.site_name = site_name
        self.base_url = base_url
        self.logger = get_logger(f"scraper.{site_name}")
        self.cache = Cache(f"{site_name}_cache")
        self.http_client = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.http_client = create_http_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.http_client:
            await self.http_client.aclose()

    @retry(
        stop=stop_after_attempt(settings.http_retries),
        wait=wait_exponential(multiplier=1, min=4, max=60)
    )
    async def fetch_page(self, url: str, **kwargs) -> str:
        """Fetch a page with retries and caching."""
        cache_key = f"page_{url}"
        
        # Check cache first
        cached_content = self.cache.get(cache_key)
        if cached_content:
            self.logger.debug(f"Using cached content for {url}")
            return cached_content

        # Rate limiting
        await asyncio.sleep(settings.rate_limit_delay)

        try:
            if self.http_client:
                response = await self.http_client.get(url, **kwargs)
                response.raise_for_status()
                content = response.text
            else:
                raise RuntimeError("HTTP client not initialized")

            # Cache the result
            self.cache.set(cache_key, content, ttl=settings.cache_ttl)
            return content

        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error {e.response.status_code} for {url}")
            raise
        except httpx.RequestError as e:
            self.logger.error(f"Request error for {url}: {e}")
            raise

    async def fetch_with_playwright(self, url: str, selector: str = None) -> str:
        """Fetch a page using Playwright for JavaScript-heavy sites."""
        cache_key = f"playwright_{url}"
        
        cached_content = self.cache.get(cache_key)
        if cached_content:
            return cached_content

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=settings.playwright_headless,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            context = await browser.new_context(
                user_agent=random.choice(settings.user_agents)
            )
            
            page = await context.new_page()
            
            # Increase timeout settings
            page.set_default_timeout(120000)  # 120 seconds for complex sites
            page.set_default_navigation_timeout(120000)
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=120000)
                
                if selector:
                    await page.wait_for_selector(selector, timeout=120000)
                
                content = await page.content()
                
                # Cache the result
                self.cache.set(cache_key, content, ttl=settings.cache_ttl)
                return content

            finally:
                await browser.close()

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content with BeautifulSoup."""
        soup = BeautifulSoup(html, "lxml")
        
        # Remove common cookie banners
        cookie_banner_selectors = [
            "#cookie-banner",
            "#cookie-notice",
            "#cookie-consent",
            ".cookie-banner",
            ".cookie-notice",
            ".cookie-consent",
            "[id*='cookie']",
            "[class*='cookie']"
        ]
        for selector in cookie_banner_selectors:
            for element in soup.select(selector):
                element.decompose()
                
        return soup

    @abstractmethod
    async def search(self, query: str) -> List[Dict[str, Any]]:
        """Search for wines on this site."""
        pass

    @abstractmethod
    async def get_wine_details(self, wine_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific wine."""
        pass

    def save_html(self, html: str, filename: str, subdir: str = None) -> Path:
        """Save HTML content to file for debugging."""
        save_dir = Path(settings.output_dir) / self.site_name
        if subdir:
            save_dir = save_dir / subdir
        
        save_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = save_dir / filename
        filepath.write_text(html, encoding="utf-8")
        
        self.logger.debug(f"Saved HTML to {filepath}")
        return filepath