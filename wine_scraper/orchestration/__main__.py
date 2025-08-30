"""Main entry point for refactored wine scraper service."""

import asyncio
import typer
from rich.console import Console

from orchestration.service import WineScraperService
from orchestration.rabbitmq import RabbitMQProducer
from pipelines.sinks import JSONSink, CSVSink
from settings import settings
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


@app.command(name="process-file")
def process_file(
    wineries_file: typer.FileText = typer.Argument(..., help="File with lines of 'url,name'"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Save results to files instead of publishing"),
    output_dir: str = typer.Option(None, "--output-dir", help="Directory for dry-run outputs (defaults to settings.OUTPUT_DIR)"),
    limit: int = typer.Option(0, "--limit", help="Optional cap on wines per winery; 0 means no cap"),
) -> None:
    """Process a file of wineries (url,name) and either publish wines or save locally."""

    # Parse file contents
    wineries: list[tuple[str, str]] = []
    for raw_line in wineries_file:
        line = raw_line.strip()
        if not line or "," not in line:
            continue
        url, name = line.split(",", 1)
        wineries.append((url.strip(), name.strip()))

    if not wineries:
        console.print("[yellow]No valid lines found. Expected format: url,name[/yellow]")
        raise typer.Exit(1)

    # Adjust output directory if requested
    if output_dir:
        settings.output_dir = output_dir
        console.print(f"[dim]Output directory set to {settings.output_dir}[/dim]")

    async def _run():
        all_wines: list = []

        if dry_run:
            # Scrape directly and save to files
            for url, name in wineries:
                console.print(f"[blue]Scraping {name} ({url})[/blue]")
                scraper = WineryScraper(name, url)
                try:
                    async with scraper:
                        wines = await scraper.scrape_winery_site()
                        if limit and limit > 0:
                            wines = wines[:limit]
                        all_wines.extend(wines)
                        console.print(f"[green]Found {len(wines)} wines from {name}[/green]")
                except Exception as e:
                    logger.error(f"Error scraping {name}", error=str(e))

            if not all_wines:
                console.print("[yellow]No wines found.[/yellow]")
                return

            # Save outputs
            json_sink = JSONSink("batch_wines.json")
            json_sink.save_wines(all_wines)
            console.print(f"[green]Saved JSON to {json_sink.filepath}[/green]")

            csv_sink = CSVSink("batch_wines.csv")
            csv_sink.save_wines(all_wines)
            console.print(f"[green]Saved CSV to {csv_sink.filepath}[/green]")
        else:
            # Scrape and publish to RabbitMQ
            producer = RabbitMQProducer()
            await producer.connect()
            try:
                for url, name in wineries:
                    console.print(f"[blue]Processing {name} ({url})[/blue]")
                    scraper = WineryScraper(name, url)
                    try:
                        async with scraper:
                            wines = await scraper.scrape_winery_site()
                            if limit and limit > 0:
                                wines = wines[:limit]
                            await producer.publish_wines(wines)
                            console.print(f"[green]Published {len(wines)} wines from {name}[/green]")
                    except Exception as e:
                        logger.error(f"Error processing {name}", error=str(e))
            finally:
                await producer.disconnect()

    asyncio.run(_run())


if __name__ == "__main__":
    app()
