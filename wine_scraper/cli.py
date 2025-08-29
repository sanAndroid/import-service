"""Command-line interface for scraperhub."""

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from scrapers.winery import WineryScraper
from pipelines.sinks import CSVSink, JSONSink
from utils.observability import get_logger

app = typer.Typer(
    name="scraperhub",
    help="Wine data scraper hub",
    add_completion=False,
)
console = Console()
logger = get_logger("cli")


@app.command()
def scrape_winery(
    url: str = typer.Argument(..., help="Winery website URL to scrape"),
    name: str = typer.Argument(..., help="Name of the winery"),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Print results to terminal instead of sending to RabbitMQ",
    ),
    output: str = typer.Option(
        "json",
        "--output",
        "-o",
        help="Output format for dry-run (json, csv, or both)",
    ),
    save_html: bool = typer.Option(
        False,
        "--save-html",
        help="Save HTML pages for debugging",
    ),
) -> None:
    """Scrape wines from a specific winery website."""
    
    async def _scrape_winery():
        scraper = WineryScraper(name, url)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            task = progress.add_task(f"Scraping {name}...", total=None)
            
            try:
                async with scraper:
                    wines = await scraper.scrape_winery_site()
                    
                    if save_html:
                        # Save HTML for debugging
                        html = await scraper.fetch_with_playwright(url)
                        scraper.save_html(html, f"{name}_index.html", "debug")
                    
                    progress.update(task, description=f"Found {len(wines)} wines from {name}")
                    
                    if not wines:
                        console.print("[yellow]No wines found.[/yellow]")
                        return
                    
                    # Handle dry-run mode
                    if dry_run:
                        console.print(f"\n[green]Found {len(wines)} wines from {name}[/green]")
                        
                        # Display results
                        table = Table(title=f"Wines from {name}")
                        table.add_column("Name", style="cyan")
                        table.add_column("Price", style="green")
                        table.add_column("Vintage", style="magenta")
                        table.add_column("Type", style="yellow")
                        
                        for wine in wines:
                            table.add_row(
                                wine.name,
                                f"${wine.price}" if wine.price else "N/A",
                                str(wine.vintage) if wine.vintage else "N/A",
                                wine.type or "N/A"
                            )
                        
                        console.print(table)
                        
                        # Save results
                        if output in ["json", "both"]:
                            json_sink = JSONSink(f"{name}_wines.json")
                            json_sink.save_wines(wines)
                            console.print(f"[green]Results saved to {json_sink.filepath}[/green]")
                        
                        if output in ["csv", "both"]:
                            csv_sink = CSVSink(f"{name}_wines.csv")
                            csv_sink.save_wines(wines)
                            console.print(f"[green]Results saved to {csv_sink.filepath}[/green]")
                    
                    else:
                        # In production mode, would send to RabbitMQ
                        # For now, just display count
                        console.print(f"[green]Found {len(wines)} wines from {name}[/green]")
                        console.print("[blue]In production, these would be sent to RabbitMQ wines queue[/blue]")
                        
                        # Save to files for testing
                        json_sink = JSONSink(f"{name}_wines.json")
                        json_sink.save_wines(wines)
                        console.print(f"[green]Results saved to {json_sink.filepath}[/green]")
                
            except Exception as e:
                console.print(f"[red]Error scraping {name}: {e}[/red]")
                logger.error(f"Error scraping {name}", error=str(e))
    
    asyncio.run(_scrape_winery())


@app.command()
def batch_scrape(
    wineries_file: Path = typer.Argument(
        ..., 
        help="File containing winery URLs and names (one per line, format: url,name)",
        exists=True,
        readable=True,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Print results to terminal instead of sending to RabbitMQ",
    ),
    output: str = typer.Option(
        "json",
        "--output",
        "-o",
        help="Output format for dry-run (json, csv, or both)",
    ),
    limit: int = typer.Option(
        50,
        "--limit",
        "-l",
        help="Maximum wines per winery",
    ),
) -> None:
    """Scrape wines from multiple winery websites."""
    
    # Read wineries from file
    try:
        with open(wineries_file, "r", encoding="utf-8") as f:
            wineries = []
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    url, name = line.split(',', 1)
                    wineries.append((url.strip(), name.strip()))
    except Exception as e:
        console.print(f"[red]Error reading wineries file: {e}[/red]")
        raise typer.Exit(1)
    
    console.print(f"Processing {len(wineries)} wineries...")
    
    async def _batch_scrape():
        all_wines = []
        
        with Progress(console=console) as progress:
            task = progress.add_task("Processing wineries...", total=len(wineries))
            
            for winery_url, winery_name in wineries:
                progress.update(task, description=f"Processing: {winery_name}")
                
                try:
                    scraper = WineryScraper(winery_name, winery_url)
                    async with scraper:
                        wines = await scraper.scrape_winery_site()
                        all_wines.extend(wines[:limit])
                        
                        if dry_run:
                            console.print(f"\n[green]Found {len(wines)} wines from {winery_name}[/green]")
                
                except Exception as e:
                    logger.error(f"Error processing {winery_name}", error=str(e))
                
                progress.advance(task)
        
        if not all_wines:
            console.print("[yellow]No wines found.[/yellow]")
            return
        
        # Handle dry-run mode
        if dry_run:
            console.print(f"\n[green]Total wines found: {len(all_wines)}[/green]")
            
            # Save results
            if output in ["json", "both"]:
                json_sink = JSONSink("batch_wines.json")
                json_sink.save_wines(all_wines)
                console.print(f"[green]Results saved to {json_sink.filepath}[/green]")
            
            if output in ["csv", "both"]:
                csv_sink = CSVSink("batch_wines.csv")
                csv_sink.save_wines(all_wines)
                console.print(f"[green]Results saved to {csv_sink.filepath}[/green]")
        else:
            console.print(f"[green]Total wines found: {len(all_wines)}[/green]")
            console.print("[blue]In production, these would be sent to RabbitMQ wines queue[/blue]")
            
            # Save to files for testing
            json_sink = JSONSink("batch_wines.json")
            json_sink.save_wines(all_wines)
            console.print(f"[green]Results saved to {json_sink.filepath}[/green]")
    
    asyncio.run(_batch_scrape())


@app.command()
def list_sources() -> None:
    """List available scraping sources."""
    table = Table(title="Available Sources")
    table.add_column("Source", style="cyan")
    table.add_column("Description", style="green")
    
    sources = [
        ("winery", "Direct winery website scraping"),
    ]
    
    for source, desc in sources:
        table.add_row(source, desc)
    
    console.print(table)


@app.command()
def service(
    rabbitmq_url: str = typer.Option(
        "amqp://rabbitmq:rabbitmq@localhost:5672/",
        "--rabbitmq-url",
        "-r",
        help="RabbitMQ connection URL",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Run in dry-run mode (no RabbitMQ)",
    ),
) -> None:
    """Start the winery scraping service (RabbitMQ mode)."""
    from orchestration.__main__ import start
    
    start(
        rabbitmq_url=rabbitmq_url,
        dry_run=dry_run,
    )


@app.command()
def clean_cache() -> None:
    """Clear all cached data."""
    from utils.cache import Cache
    
    cache = Cache("main")
    cache.clear()
    console.print("[green]Cache cleared successfully[/green]")


def main() -> None:
    """Main entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
