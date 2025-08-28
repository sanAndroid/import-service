"""Application settings using Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # RabbitMQ settings
    rabbitmq_host: str = Field(default="localhost", env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(default=5672, env="RABBITMQ_PORT")
    rabbitmq_user: str = Field(default="guest", env="RABBITMQ_USER")
    rabbitmq_password: str = Field(default="guest", env="RABBITMQ_PASSWORD")
    rabbitmq_wineries_queue: str = Field(default="wineries", env="RABBITMQ_WINERIES_QUEUE")
    rabbitmq_wines_exchange: str = Field(default="wines", env="RABBITMQ_WINES_EXCHANGE")
    rabbitmq_winery_routing_key: str = Field(default="winery.#", env="RABBITMQ_WINERY_ROUTING_KEY")
    rabbitmq_wine_scraped_routing_key: str = Field(default="wine.scraped", env="RABBITMQ_WINE_SCRAPED_ROUTING_KEY")

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
