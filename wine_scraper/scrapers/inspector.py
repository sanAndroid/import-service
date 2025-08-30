import asyncio
import re
from typing import Dict, Optional

import yaml
from bs4 import BeautifulSoup
from playwright.async_api import Page, async_playwright

from utils.observability import get_logger

logger = get_logger("scraper.inspector")

class Inspector:
    def __init__(self, url: str):
        self.url = url
        self.page: Optional[Page] = None
        self.soup: Optional[BeautifulSoup] = None

    async def inspect(self) -> str:
        """
        Inspects a given URL to generate a draft scraper configuration.
        """
        browser = None
        try:
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=True)
            self.page = await browser.new_page()
            await self.page.goto(self.url, wait_until="networkidle", timeout=60000)
            
            html = await self.page.content()
            self.soup = BeautifulSoup(html, "html.parser")

            config = {
                'start_url': self.url,
                'selectors': {
                    'name': self._find_name_selector(),
                    'price': self._find_price_selector(),
                    'description': '# To be filled in manually',
                    'image_url': '# To be filled in manually',
                }
            }
            
            return yaml.dump(config, default_flow_style=False, sort_keys=False)

        except Exception as e:
            logger.error(f"Failed to inspect {self.url}: {e}")
            return f"# Failed to inspect {self.url}: {e}"
        finally:
            if browser:
                await browser.close()

    def _find_name_selector(self) -> str:
        """Heuristically finds a CSS selector for the product name."""
        if not self.soup:
            return ""
        
        h1 = self.soup.find("h1")
        if h1:
            selector = "h1"
            if h1.get('class'):
                selector = f"h1.{'.'.join(h1.get('class'))}"
            return selector
            
        return "# Fallback: No <h1> found"

    def _find_price_selector(self) -> str:
        """Heuristically finds a CSS selector for the price."""
        if not self.soup:
            return ""
            
        price_regex = re.compile(r'(€|EUR|\$|price)', re.IGNORECASE)
        price_element = self.soup.find(string=price_regex)
        
        if price_element:
            parent = price_element.parent
            if parent:
                selector = parent.name
                if parent.get('class'):
                    selector = f"{selector}.{'.'.join(parent.get('class'))}"
                if parent.parent:
                    parent_selector = parent.parent.name
                    if parent.parent.get('class'):
                        parent_selector = f"{parent_selector}.{'.'.join(parent.parent.get('class'))}"
                    return f"{parent_selector} > {selector}"
                return selector

        return "# Fallback: No price element found"
