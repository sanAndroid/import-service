"""Application settings using Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # RabbitMQ settings
    rabbitmq_host: str = Field(default="localhost", env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(default=5672, env="RABBITMQ_PORT")
    rabbitmq_user: str = Field(default="rabbitmq", env="RABBITMQ_USER")
    rabbitmq_password: str = Field(default="rabbitmq", env="RABBITMQ_PASSWORD")
    rabbitmq_wineries_queue: str = Field(default="wineries_message", env="RABBITMQ_WINERIES_QUEUE")
    rabbitmq_wines_exchange: str = Field(default="wines", env="RABBITMQ_WINES_EXCHANGE")
    rabbitmq_winery_routing_key: str = Field(default="winery.#", env="RABBITMQ_WINERY_ROUTING_KEY")
    rabbitmq_wine_scraped_routing_key: str = Field(default="wine.scraped", env="RABBITMQ_WINE_SCRAPED_ROUTING_KEY")

    # Scraper settings
    # Discovery crawler settings
    # Increased default depth to explore deeper category → product paths
    scraper_max_crawl_depth: int = Field(default=8, env="SCRAPER_MAX_CRAWL_DEPTH")
    scraper_max_urls_per_domain: int = Field(default=100, env="SCRAPER_MAX_URLS_PER_DOMAIN")
    scraper_default_timeout: int = Field(default=120000, env="SCRAPER_DEFAULT_TIMEOUT")
    scraper_content_score_threshold: int = Field(default=5, env="SCRAPER_CONTENT_SCORE_THRESHOLD")

    # URL classifier threshold for accepting a page as a wine product URL
    url_classifier_threshold: float = Field(default=0.8, env="URL_CLASSIFIER_THRESHOLD")

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
