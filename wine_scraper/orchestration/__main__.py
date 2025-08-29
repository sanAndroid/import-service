"""Main entry point for refactored wine scraper service."""

import asyncio
import typer
from rich.console import Console

from orchestration.service import WineScraperService
from utils.observability import get_logger

app = typer.Typer(
    name="wine-scraper",
    help="Wine scraper service with proper message handling",
    add_completion=False,
)
console = Console()
logger = get_logger("wine-scraper")


@app.command()
def start(
    once: bool = typer.Option(
        False,
        "--once",
        help="Process one message then exit",
    )
) -> None:
    """Start the wine scraper service."""
    
    async def _start_service():
        service = WineScraperService()
        
        if once:
            logger.info("Running in single-message mode")
            console.print("[blue]Processing one winery message...[/blue]")
            await service.run_once()
        else:
            logger.info("Starting continuous service")
            console.print("[green]Starting wine scraper service...[/green]")
            console.print("[dim]Connected to RabbitMQ. Waiting for wineries...[/dim]")
            await service.run()
    
    asyncio.run(_start_service())


if __name__ == "__main__":
    app()