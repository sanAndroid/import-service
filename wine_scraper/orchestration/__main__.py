"""Main entry point for RabbitMQ-based winery scraping service."""

import asyncio
import os
from typing import List

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from orchestration.rabbitmq import RabbitMQManager
from scrapers.winery import WineryScraper
from utils.observability import get_logger

app = typer.Typer(
    name="winery-scraper",
    help="RabbitMQ-based winery scraping service",
    add_completion=False,
)
console = Console()
logger = get_logger("winery-scraper")


@app.command()
def start(
    rabbitmq_url: str = typer.Option(
        "amqp://guest:guest@localhost:5672/",
        "--rabbitmq-url",
        "-r",
        help="RabbitMQ connection URL",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Print results to terminal instead of sending to RabbitMQ",
    ),
    output_dir: str = typer.Option(
        "./data",
        "--output-dir",
        "-d",
        help="Output directory for dry-run results",
    ),
) -> None:
    """Start the RabbitMQ winery scraping service."""
    
    async def _start_service():
        if dry_run:
            logger.info("Starting in dry-run mode")
            console.print("[blue]Starting winery scraper in dry-run mode[/blue]")
            
            # For dry-run, we'll just wait for wineries via stdin
            console.print("[yellow]Enter winery URLs and names (format: url,name), one per line. Type 'done' to finish:[/yellow]")
            
            wineries = []
            while True:
                line = input().strip()
                if line.lower() == 'done':
                    break
                if ',' in line:
                    url, name = line.split(',', 1)
                    wineries.append((url.strip(), name.strip()))
            
            if not wineries:
                console.print("[yellow]No wineries provided. Exiting.[/yellow]")
                return
            
            console.print(f"[green]Processing {len(wineries)} wineries...[/green]")
            
            with Progress(console=console) as progress:
                task = progress.add_task("Processing wineries...", total=len(wineries))
                
                for winery_url, winery_name in wineries:
                    try:
                        scraper = WineryScraper(winery_name, winery_url)
                        async with scraper:
                            wines = await scraper.scrape_winery_site()
                            
                            console.print(f"\n[green]Found {len(wines)} wines from {winery_name}[/green]")
                            
                            if wines:
                                from pipelines.sinks import JSONSink
                                os.makedirs(output_dir, exist_ok=True)
                                json_sink = JSONSink(f"{output_dir}/{winery_name}_wines.json")
                                json_sink.save_wines(wines)
                                console.print(f"[green]Saved to {json_sink.filepath}[/green]")
                    
                    except Exception as e:
                        logger.error(f"Error processing {winery_name}", error=str(e))
                        console.print(f"[red]Error processing {winery_name}: {e}[/red]")
                    
                    progress.advance(task)
            
        else:
            logger.info("Starting RabbitMQ service")
            console.print("[blue]Starting winery scraper with RabbitMQ integration[/blue]")
            
            try:
                async with RabbitMQManager(rabbitmq_url) as mq_manager:
                    
                    async def process_winery(winery_msg):
                        """Process a single winery message."""
                        scraper = WineryScraper(winery_msg.name, winery_msg.url)
                        
                        try:
                            async with scraper:
                                wines = await scraper.scrape_winery_site()
                                
                                if wines:
                                    await mq_manager.producer.publish_wines(wines)
                                    logger.info(f"Published {len(wines)} wines from {winery_msg.name}")
                                else:
                                    logger.info(f"No wines found for {winery_msg.name}")
                        
                        except Exception as e:
                            logger.error(f"Error processing winery {winery_msg.name}", error=str(e))
                    
                    console.print("[green]Connected to RabbitMQ. Waiting for wineries...[/green]")
                    await mq_manager.process_wineries(process_winery)
            
            except Exception as e:
                logger.error("Failed to start service", error=str(e))
                console.print(f"[red]Failed to start service: {e}[/red]")
    
    asyncio.run(_start_service())


@app.command()
def process_file(
    wineries_file: str = typer.Argument(..., help="File containing winery URLs and names"),
    rabbitmq_url: str = typer.Option(
        "amqp://guest:guest@localhost:5672/",
        "--rabbitmq-url",
        "-r",
        help="RabbitMQ connection URL",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Print results to terminal instead of sending to RabbitMQ",
    ),
    output_dir: str = typer.Option(
        "./data",
        "--output-dir",
        "-d",
        help="Output directory for dry-run results",
    ),
) -> None:
    """Process wineries from a file."""
    
    async def _process_file():
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
        
        if not wineries:
            console.print("[yellow]No wineries found in file.[/yellow]")
            return
        
        console.print(f"Processing {len(wineries)} wineries...")
        
        if dry_run:
            with Progress(console=console) as progress:
                task = progress.add_task("Processing wineries...", total=len(wineries))
                
                for winery_url, winery_name in wineries:
                    try:
                        scraper = WineryScraper(winery_name, winery_url)
                        async with scraper:
                            wines = await scraper.scrape_winery_site()
                            
                            console.print(f"\n[green]Found {len(wines)} wines from {winery_name}[/green]")
                            
                            if wines:
                                from pipelines.sinks import JSONSink
                                os.makedirs(output_dir, exist_ok=True)
                                json_sink = JSONSink(f"{output_dir}/{winery_name}_wines.json")
                                json_sink.save_wines(wines)
                                console.print(f"[green]Saved to {json_sink.filepath}[/green]")
                    
                    except Exception as e:
                        logger.error(f"Error processing {winery_name}", error=str(e))
                        console.print(f"[red]Error processing {winery_name}: {e}[/red]")
                    
                    progress.advance(task)
        
        else:
            # Production mode with RabbitMQ
            try:
                async with RabbitMQManager(rabbitmq_url) as mq_manager:
                    with Progress(console=console) as progress:
                        task = progress.add_task("Processing wineries...", total=len(wineries))
                        
                        for winery_url, winery_name in wineries:
                            try:
                                scraper = WineryScraper(winery_name, winery_url)
                                async with scraper:
                                    wines = await scraper.scrape_winery_site()
                                    
                                    if wines:
                                        await mq_manager.producer.publish_wines(wines)
                                        logger.info(f"Published {len(wines)} wines from {winery_name}")
                                        console.print(f"[green]Published {len(wines)} wines from {winery_name}[/green]")
                                    else:
                                        logger.info(f"No wines found for {winery_name}")
                                        console.print(f"[yellow]No wines found for {winery_name}[/yellow]")
                            
                            except Exception as e:
                                logger.error(f"Error processing {winery_name}", error=str(e))
                                console.print(f"[red]Error processing {winery_name}: {e}[/red]")
                            
                            progress.advance(task)
            
            except Exception as e:
                logger.error("Failed to connect to RabbitMQ", error=str(e))
                console.print(f"[red]Failed to connect to RabbitMQ: {e}[/red]")
    
    asyncio.run(_process_file())


if __name__ == "__main__":
    app()