#!/usr/bin/env python3
"""
Standalone JSON Schema generator for Wine model.

This script generates a JSON Schema from a simplified Wine model
without importing the full project dependencies.
"""

import json
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class WineRating(BaseModel):
    """Wine rating information."""
    
    source: str = Field(..., description="Source of the rating (e.g., vivino, wine_searcher)")
    rating: Optional[float] = Field(None, description="Average rating")
    ratings_count: Optional[int] = Field(None, description="Number of ratings")
    critics_rating: Optional[float] = Field(None, description="Average critic rating")
    critics_count: Optional[int] = Field(None, description="Number of critic ratings")


class Wine(BaseModel):
    """Wine data model for cross-language DTO generation."""
    
    name: str = Field(..., description="Wine name")
    winery: str = Field(..., description="Winery/Producer name")
    winery_website: str = Field(..., description="Base winery website URL (e.g., https://www.weingut-rainer-sauer.de)")
    type: Optional[str] = Field(None, description="Wine type (red, white, rosé, etc.)")
    region: Optional[str] = Field(None, description="Wine region")
    country: Optional[str] = Field(None, description="Country of origin")
    grapes: Optional[List[str]] = Field(None, description="Grape varieties")
    alcohol_content: Optional[float] = Field(None, description="Alcohol content percentage")
    vintage: Optional[int] = Field(None, description="Vintage year")
    
    # Pricing
    price: Optional[float] = Field(None, description="Current price")
    price_range: Optional[str] = Field(None, description="Price range")
    currency: Optional[str] = Field(None, description="Currency")
    
    # CLAUDE.md required fields
    description: Optional[str] = Field(None, description="Wine description")
    quality_level: Optional[str] = Field(None, description="Quality level (e.g., Großes Gewächs, Grand Cru)")
    shop_url: Optional[str] = Field(None, description="Direct link to the wine's product page")
    bottle_size: Optional[str] = Field(None, description="Bottle size (e.g., 750ml, 1.5L)")
    average_rating: Optional[float] = Field(None, description="Average rating/score")
    number_of_ratings: Optional[int] = Field(None, description="Number of ratings")
    critic_scores: Optional[Dict[str, float]] = Field(None, description="Critic scores by source")
    food_pairings: Optional[List[str]] = Field(None, description="Recommended food pairings")
    serving_temperature: Optional[str] = Field(None, description="Recommended serving temperature")
    availability_status: Optional[str] = Field(None, description="Availability status")
    sku: Optional[str] = Field(None, description="SKU/Product ID")
    
    # Ratings
    ratings: List[WineRating] = Field(default_factory=list, description="List of ratings from different sources")
    
    # Media
    image_url: Optional[str] = Field(None, description="Wine image URL")
    
    # Metadata
    source_urls: List[str] = Field(default_factory=list, description="Source URLs")
    scraped_at: Optional[str] = Field(None, description="When this data was scraped")


def generate_json_schema():
    """Generate JSON Schema from the Wine model."""
    try:
        # Generate schema using Pydantic v2 method
        schema = Wine.model_json_schema()
        
        # Add metadata
        schema['$schema'] = "http://json-schema.org/draft-07/schema#"
        schema['title'] = "Wine"
        schema['description'] = "Wine data model for cross-language DTO generation"
        
        # Write schema to file
        schema_file = "wine-schema.json"
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON Schema generated: {schema_file}")
        print(f"📄 Schema includes {len(schema.get('properties', {}))} properties")
        
        # Also print to console for quick reference
        print("\n📋 Full JSON Schema:")
        print(json.dumps(schema, indent=2))
        
        return schema_file
        
    except Exception as e:
        print(f"❌ Error generating schema: {e}")
        return None

if __name__ == "__main__":
    generate_json_schema()