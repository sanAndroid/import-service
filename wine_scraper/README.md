# Winery Scraper Service

[![version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/jcampos/wine-scraper/releases)

A production-ready service for scraping wine data from winery websites using RabbitMQ for message processing.

## Overview

This service consumes winery URLs from a RabbitMQ queue (`wineries`), scrapes each winery's website for wine information, and publishes the extracted data to a RabbitMQ exchange (`wines`). It supports both production mode (with RabbitMQ) and dry-run mode for development/testing.

## Features

- **RabbitMQ Integration**: Full message queue processing with durable queues and exchanges
- **Direct Winery Scraping**: Scrapes winery websites for wine products
- **Comprehensive Data**: Extracts 21+ wine attributes including name, price, vintage, grapes, ratings, etc.
- **Dry-run Mode**: Test scraping without RabbitMQ
- **Multiple Output Formats**: JSON, CSV, and Parquet
- **Caching**: Built-in caching for scraped data
- **Playwright Support**: Handles JavaScript-heavy sites
- **Rich CLI**: Progress bars and formatted output
- **Error Handling**: Robust error handling and logging

## Quick Start

### 1. Install Dependencies

```bash
# Clone and enter directory
git clone https://github.com/jcampos/wine-scraper.git
cd wine-scraper/apps/transformer-service/wine_scraper

# Install with make (recommended)
make install

# Or manually
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Configure Environment

Create a `.env` file in the project root:

```bash
# RabbitMQ Configuration
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# Logging
LOG_LEVEL=INFO

# HTTP Settings
HTTP_TIMEOUT=30
HTTP_RETRIES=3

# Playwright
PLAYWRIGHT_HEADLESS=true

# Cache
CACHE_DIR=".cache"
CACHE_TTL=3600

# Output
OUTPUT_DIR="data"
```

## Usage

### Production Mode (with RabbitMQ)

Start the service to process wineries from the RabbitMQ queue:

```bash
# Default RabbitMQ connection
make run-service

# Custom RabbitMQ URL
make run-service RABBITMQ_URL=amqp://user:pass@localhost:5672/
```

### Development/Testing

#### Dry-run Mode (Interactive)
```bash
make run-dry-run
# Then enter wineries in format: url,name
# Example: https://www.weingut-rainer-sauer.de/,Weingut Rainer Sauer
# Type 'done' when finished
```

#### Batch Processing from File
```bash
# Create test file
echo "https://www.weingut-rainer-sauer.de/,Weingut Rainer Sauer
https://www.buerklin-wolf.de/,Bürklin-Wolf" > test_wineries.txt

# Run batch scrape
make run-batch-test

# Or with custom file
python cli.py batch-scrape wineries.txt --dry-run
```

#### Single Winery Test
```bash
make run-single

# Or specific winery
python cli.py scrape-winery https://www.weingut-rainer-sauer.de/ "Weingut Rainer Sauer" --dry-run
```

### CLI Commands

```bash
# List all commands
python cli.py --help

# Clean cache
python cli.py clean-cache

# Scrape single winery
python cli.py scrape-winery URL "Winery Name" --dry-run

# Batch scrape from file
python cli.py batch-scrape wineries.txt --dry-run --output json
```

## Data Structure

Each wine includes these fields:
- **Basic Info**: name, winery, vintage, price, description, wine_type
- **Technical**: grapes, region, country, alcohol_content, bottle_size
- **Visual**: image_url, quality_level
- **Ratings**: average_rating, number_of_ratings, critic_scores
- **Commercial**: shop_url, availability_status, sku/product_id
- **Details**: food_pairings, serving_temperature

## RabbitMQ Configuration

### Input (Wineries Queue)
- **Queue**: `wineries`
- **Message Format**: `{"url": "https://winery.com", "name": "Winery Name"}`

### Output (Wines Exchange)
- **Exchange**: `wines` (Topic)
- **Routing Key**: `wine.scraped`
- **Message**: Full wine data as JSON

### Setup RabbitMQ

```bash
# Start RabbitMQ with Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Access management UI at http://localhost:15672 (guest/guest)
```

## Project Structure

```
.
├── orchestration/          # RabbitMQ service
│   ├── rabbitmq.py        # RabbitMQ integration
│   └── __main__.py        # Service entry point
├── scrapers/              # Scraping logic
│   ├── base.py           # Base scraper class
│   └── winery.py         # Winery website scraper
├── pipelines/            # Data processing
│   ├── models.py         # Wine data models
│   └── sinks/            # Data storage (JSON, CSV, Parquet)
├── utils/                # Utilities
│   ├── cache.py          # Caching
│   ├── http.py           # HTTP client
│   └── observability.py  # Logging and metrics
├── cli.py               # Command-line interface
├── Makefile            # Build automation
├── requirements.txt    # Dependencies
└── test_wineries.txt   # Sample wineries
```

## Make Commands

```bash
make install          # Install dependencies
make run-service      # Start RabbitMQ service
make run-dry-run      # Interactive dry-run mode
make run-batch-test   # Test batch scraping
make run-single       # Test single winery
make clean           # Clean cache and temp files
make lint            # Run linting
make test            # Run basic tests
```

## Troubleshooting

### Common Issues

1. **"lxml not found"**: Install with `pip install lxml`
2. **"Playwright not found"**: Run `playwright install chromium`
3. **RabbitMQ connection**: Ensure RabbitMQ is running at the configured URL
4. **Import errors**: Activate virtual environment with `source venv/bin/activate`

### Debug Mode

```bash
# Enable debug logging
LOG_LEVEL=DEBUG make run-dry-run

# Save HTML for debugging
python cli.py scrape-winery URL "Name" --dry-run --save-html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new scrapers
4. Run `make test` and `make lint`
5. Submit a pull request

## License

This project is licensed under the MIT License.
