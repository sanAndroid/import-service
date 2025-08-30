import re
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class WineDataExtractor:
    def __init__(self, soup: BeautifulSoup, url: str):
        self.soup = soup
        self.url = url

    def extract_all(self) -> Dict[str, Any]:
        wine_data = {
            'name': self.extract_wine_name(),
            'price': self.extract_price(),
            'currency': self.extract_currency(),
            'description': self.extract_description(),
            'vintage': self.extract_vintage(),
            'grapes': self.extract_grape_varieties(),
            'region': self.extract_region(),
            'country': self.extract_country(),
            'type': self.extract_wine_type(),
            'alcohol_content': self.extract_alcohol_content(),
            'image_url': self.extract_image_url(),
            'quality_level': self.extract_quality_level(),
            'bottle_size': self.extract_bottle_size(),
            'average_rating': self.extract_average_rating(),
            'number_of_ratings': self.extract_number_of_ratings(),
            'critic_scores': self.extract_critic_scores(),
            'food_pairings': self.extract_food_pairings(),
            'serving_temperature': self.extract_serving_temperature(),
            'availability_status': self.extract_availability_status(),
            'sku': self.extract_sku()
        }
        return {k: v for k, v in wine_data.items() if v is not None}

    def extract_wine_name(self) -> Optional[str]:
        selectors = [
            "h1",
            ".product-title",
            ".wine-name",
            "[class*='wine-title']",
            "[class*='product-name']",
            "meta[property='og:title']"
        ]
        for selector in selectors:
            element = self.soup.select_one(selector)
            if element:
                if selector == "meta[property='og:title']":
                    return element.get('content', '').strip()
                return element.get_text(strip=True)
        return self.url.split('/')[-1].replace('-', ' ').replace('_', ' ').title()

    def extract_price(self) -> Optional[float]:
        price_selectors = [
            ".price",
            ".product-price",
            "[class*='price']",
            "meta[property='product:price:amount']"
        ]
        for selector in price_selectors:
            elements = self.soup.select(selector)
            for element in elements:
                text = element.get_text() if hasattr(element, 'get_text') else str(element)
                if text:
                    # This regex is designed to handle various European and American price formats.
                    # It looks for numbers with optional commas or dots as thousands separators,
                    # and a comma or dot as a decimal separator.
                    price_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?|\d+(?:[.,]\d{2})?)', text)
                    if price_match:
                        price_str = price_match.group(1)
                        # Normalize the number format by removing thousands separators and replacing the decimal comma with a dot.
                        price_str = price_str.replace('.', '').replace(',', '.')
                        try:
                            return float(price_str)
                        except ValueError:
                            continue
        return None

    def extract_currency(self) -> Optional[str]:
        text = self.soup.get_text()
        currency_match = re.search(r'(€|\$|£|CHF|¥|R)', text)
        if currency_match:
            return currency_match.group(1)
        return None

    def extract_description(self) -> Optional[str]:
        description_selectors = [
            ".description",
            ".product-description",
            "[class*='description']",
            "meta[property='og:description']",
            ".wine-notes",
            ".tasting-notes"
        ]
        for selector in description_selectors:
            element = self.soup.select_one(selector)
            if element:
                if selector == "meta[property='og:description']":
                    return element.get('content', '').strip()
                return element.get_text(strip=True)
        return None

    def extract_vintage(self) -> Optional[int]:
        text = self.soup.get_text()
        year_match = re.search(r'\b(199\d|20\d{2})\b', text)
        if year_match:
            try:
                return int(year_match.group())
            except ValueError:
                pass
        return None

    def extract_grape_varieties(self) -> Optional[List[str]]:
        grape_selectors = [
            ".grape",
            ".varietal",
            ".grape-variety",
            "[class*='grape']",
            "[class*='varietal']"
        ]
        for selector in grape_selectors:
            elements = self.soup.select(selector)
            if elements:
                varieties = []
                for element in elements:
                    text = element.get_text(strip=True)
                    if text:
                        varieties.extend([v.strip() for v in text.split(',')])
                return varieties
        return None

    def extract_region(self) -> Optional[str]:
        region_selectors = [
            ".region",
            ".wine-region",
            "[class*='region']",
            ".origin"
        ]
        for selector in region_selectors:
            element = self.soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None

    def extract_country(self) -> Optional[str]:
        country_selectors = [
            ".country",
            ".origin-country",
            "[class*='country']"
        ]
        for selector in country_selectors:
            element = self.soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None

    def extract_wine_type(self) -> Optional[str]:
        type_selectors = [
            ".wine-type",
            ".type",
            "[class*='type']"
        ]
        for selector in type_selectors:
            element = self.soup.select_one(selector)
            if element:
                wine_type = element.get_text(strip=True).lower()
                if any(t in wine_type for t in ['red', 'white', 'rosé', 'sparkling', 'dessert']):
                    return wine_type.title()
        description = self.extract_description()
        if description:
            description_lower = description.lower()
            if 'red' in description_lower: return "Red"
            elif 'white' in description_lower: return "White"
            elif 'rosé' in description_lower or 'rose' in description_lower: return "Rosé"
            elif 'sparkling' in description_lower or 'champagne' in description_lower: return "Sparkling"
        return None

    def extract_alcohol_content(self) -> Optional[float]:
        text = self.soup.get_text()
        # More robust regex for alcohol content
        alcohol_match = re.search(r'(?:Alcohol|Alkoholgehalt)?\s*\(?%?\s*Vol\.?\)?[:\s]*(\d+(?:[.,]\d+)?)%?', text, re.IGNORECASE)
        if alcohol_match:
            try:
                return float(alcohol_match.group(1).replace(',', '.'))
            except ValueError:
                pass
        return None

    def extract_image_url(self) -> Optional[str]:
        image_selectors = [
            ".product-image img",
            ".wine-image img",
            "img[src*='wine']",
            "meta[property='og:image']"
        ]
        for selector in image_selectors:
            element = self.soup.select_one(selector)
            if element:
                src = element.get('content') if selector == "meta[property='og:image']" else element.get('src')
                if src:
                    return urljoin(self.url, src)
        return None

    def extract_quality_level(self) -> Optional[str]:
        text = self.soup.get_text()
        quality_indicators = ["Großes Gewächs", "Grand Cru", "Ortswein", "Gutswein", "Premier Cru", "Classico", "Riserva", "Gran Riserva"]
        for indicator in quality_indicators:
            if indicator.lower() in text.lower():
                return indicator
        return None

    def extract_bottle_size(self) -> Optional[str]:
        text = self.soup.get_text()
        size_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(ml|l|cl)', text, re.IGNORECASE)
        if size_match:
            return f"{size_match.group(1)}{size_match.group(2).upper()}"
        return "750ml"

    def extract_average_rating(self) -> Optional[float]:
        return None

    def extract_number_of_ratings(self) -> Optional[int]:
        return None

    def extract_critic_scores(self) -> Optional[Dict[str, float]]:
        return None

    def extract_food_pairings(self) -> Optional[List[str]]:
        pairing_selectors = [".food-pairing", ".pairing", "[class*='pairing']", ".serving-suggestions"]
        for selector in pairing_selectors:
            element = self.soup.select_one(selector)
            if element:
                text = element.get_text()
                foods = re.split(r'[\,\n]+', text)
                return [food.strip() for food in foods if food.strip()]
        return None

    def extract_serving_temperature(self) -> Optional[str]:
        temp_selectors = [".serving-temperature", ".temperature", "[class*='temp']"]
        for selector in temp_selectors:
            element = self.soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None

    def extract_availability_status(self) -> Optional[str]:
        availability_selectors = [".availability", ".stock", ".in-stock", ".out-of-stock"]
        for selector in availability_selectors:
            element = self.soup.select_one(selector)
            if element:
                text = element.get_text(strip=True).lower()
                if 'out' in text or 'unavailable' in text: return "Out of Stock"
                elif 'in' in text or 'available' in text: return "In Stock"
                else: return text.title()
        return None

    def extract_sku(self) -> Optional[str]:
        sku_selectors = [".sku", ".product-id", ".item-id", "[data-sku]", "[class*='sku']"]
        for selector in sku_selectors:
            element = self.soup.select_one(selector)
            if element:
                return element.get_text(strip=True) or element.get('data-sku')
        return None