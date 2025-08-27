"""Pydantic models for structured wine data."""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field, validator


class WineRating(BaseModel):
    """Wine rating information."""
    
    source: str = Field(..., description="Source of the rating (e.g., vivino, wine_searcher)")
    rating: Optional[float] = Field(None, description="Average rating")
    ratings_count: Optional[int] = Field(None, description="Number of ratings")
    critics_rating: Optional[float] = Field(None, description="Average critic rating")
    critics_count: Optional[int] = Field(None, description="Number of critic ratings")


class Wine(BaseModel):
    """Wine data model."""
    
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
    
    @validator('price')
    def validate_price(cls, v):
        """Validate price is non-negative."""
        if v is not None and v < 0:
            raise ValueError('Price must be non-negative')
        return v
    
    @validator('alcohol_content')
    def validate_alcohol(cls, v):
        """Validate alcohol content is reasonable."""
        if v is not None and (v < 5 or v > 25):
            raise ValueError('Alcohol content should be between 5% and 25%')
        return v
    
    def get_rating(self, source: str) -> Optional[float]:
        """Get rating for a specific source."""
        for rating in self.ratings:
            if rating.source == source:
                return rating.rating
        return None
    
    def get_best_rating(self) -> Optional[float]:
        """Get the highest rating from all sources."""
        if not self.ratings:
            return None
        return max((r.rating for r in self.ratings if r.rating is not None), default=None)


class ScrapingResult(BaseModel):
    """Result of a scraping operation."""
    
    query: str = Field(..., description="Search query")
    wines: List[Wine] = Field(default_factory=list, description="List of found wines")
    source: str = Field(..., description="Source that was scraped")
    success: bool = Field(..., description="Whether scraping was successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    wines_found: int = Field(..., description="Number of wines found")
    
    class Config:
        json_encoders = {
            Wine: lambda v: v.dict(),
        }