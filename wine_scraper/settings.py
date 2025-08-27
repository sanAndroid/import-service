"""Configuration settings for scraperhub."""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # General settings
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # HTTP settings
    http_timeout: int = Field(default=30, env="HTTP_TIMEOUT")
    http_retries: int = Field(default=3, env="HTTP_RETRIES")
    user_agents: list[str] = Field(
        default=[
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:118.0) Gecko/20100101 Firefox/118.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        ],
        env="USER_AGENTS"
    )
    
    # Playwright settings
    playwright_headless: bool = Field(default=True, env="PLAYWRIGHT_HEADLESS")
    playwright_slow_mo: int = Field(default=300, env="PLAYWRIGHT_SLOW_MO")
    
    # Cache settings
    cache_dir: str = Field(default=".cache", env="CACHE_DIR")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    
    # Rate limiting
    rate_limit_delay: float = Field(default=1.0, env="RATE_LIMIT_DELAY")
    
    # Data output settings
    output_dir: str = Field(default="data", env="OUTPUT_DIR")
    csv_filename: str = Field(default="wines.csv", env="CSV_FILENAME")
    
    # Wine sites configuration
    vivino_base_url: str = Field(default="https://www.vivino.com", env="VIVINO_BASE_URL")
    wine_searcher_base_url: str = Field(default="https://www.wine-searcher.com", env="WINE_SEARCHER_BASE_URL")
    
    # OpenAI settings (for legacy support)
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()