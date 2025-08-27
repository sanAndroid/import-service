"""Data transformation utilities."""

import re
from typing import Dict, Any, List
from datetime import datetime

from .models import Wine, WineRating


class DataTransformer:
    """Transform raw scraped data into structured wine data."""

    @staticmethod
    def transform_vivino_data(raw_data: Dict[str, Any]) -> Wine:
        """Transform Vivino raw data into Wine model."""
        wine = Wine(
            name=raw_data.get("name", "N/A"),
            winery=raw_data.get("winery", "N/A"),
            image_url=raw_data.get("image_url"),
            source_urls=[raw_data.get("url", "")],
            scraped_at=datetime.now().isoformat(),
        )
        
        # Add rating
        if raw_data.get("rating") is not None:
            wine.ratings.append(
                WineRating(
                    source="vivino",
                    rating=raw_data.get("rating"),
                    ratings_count=raw_data.get("ratings_count", 0),
                )
            )
        
        return wine

    @staticmethod
    def transform_wine_searcher_data(raw_data: Dict[str, Any]) -> Wine:
        """Transform Wine-Searcher raw data into Wine model."""
        wine = Wine(
            name=raw_data.get("name", "N/A"),
            winery=raw_data.get("producer", "N/A"),
            region=raw_data.get("region"),
            price_range=raw_data.get("price_range"),
            source_urls=[raw_data.get("url", "")],
            scraped_at=datetime.now().isoformat(),
        )
        
        # Add ratings
        ratings = WineRating(
            source="wine_searcher",
            rating=raw_data.get("avg_user"),
            ratings_count=raw_data.get("user_count"),
            critics_rating=raw_data.get("avg_critics"),
            critics_count=raw_data.get("critics_count"),
        )
        wine.ratings.append(ratings)
        
        return wine

    @staticmethod
    def clean_price(price_str: str) -> float:
        """Clean and parse price string to float."""
        if not price_str or price_str == "N/A":
            return 0.0
        
        # Remove currency symbols and spaces, extract number
        cleaned = re.sub(r'[^\d.,]', '', price_str)
        cleaned = cleaned.replace(',', '')
        
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    @staticmethod
    def extract_vintage(name: str) -> int:
        """Extract vintage year from wine name."""
        match = re.search(r'\b(19|20)\d{2}\b', name)
        if match:
            return int(match.group())
        return None

    @staticmethod
    def extract_grapes(description: str) -> List[str]:
        """Extract grape varieties from description."""
        common_grapes = [
            "cabernet sauvignon", "merlot", "pinot noir", "chardonnay", 
            "sauvignon blanc", "riesling", "syrah", "shiraz", "malbec",
            "tempranillo", "sangiovese", "nebbiolo", "zinfandel", "grenache",
            "mourvèdre", "petit verdot", "cabernet franc", "pinot grigio",
            "gewürztraminer", "viognier", "semillon", "chenin blanc"
        ]
        
        if not description:
            return []
        
        description_lower = description.lower()
        found_grapes = []
        
        for grape in common_grapes:
            if grape in description_lower:
                found_grapes.append(grape.title())
        
        return found_grapes

    @staticmethod
    def standardize_wine_type(wine_type: str) -> str:
        """Standardize wine type names."""
        type_mapping = {
            "rot": "red",
            "red wine": "red",
            "weiss": "white",
            "white wine": "white",
            "rosé": "rosé",
            "rose": "rosé",
            "sparkling": "sparkling",
            "dessert": "dessert",
            "fortified": "fortified",
        }
        
        if not wine_type:
            return None
        
        wine_type_lower = wine_type.lower()
        return type_mapping.get(wine_type_lower, wine_type)

    @staticmethod
    def merge_wine_data(wines: List[Wine]) -> Wine:
        """Merge wine data from multiple sources."""
        if not wines:
            return None
        
        # Use the first wine as base
        base_wine = wines[0]
        
        # Merge ratings from all sources
        all_ratings = []
        source_urls = []
        
        for wine in wines:
            all_ratings.extend(wine.ratings)
            source_urls.extend(wine.source_urls)
        
        # Create merged wine
        merged = Wine(
            name=base_wine.name,
            winery=base_wine.winery,
            type=base_wine.type,
            region=base_wine.region,
            country=base_wine.country,
            grapes=base_wine.grapes,
            alcohol_content=base_wine.alcohol_content,
            vintage=base_wine.vintage,
            price=base_wine.price,
            price_range=base_wine.price_range,
            currency=base_wine.currency,
            image_url=base_wine.image_url,
            ratings=all_ratings,
            source_urls=list(set(source_urls)),  # Remove duplicates
            scraped_at=datetime.now().isoformat(),
        )
        
        return merged