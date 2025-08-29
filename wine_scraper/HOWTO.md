# How-To Guide

This guide provides detailed instructions on how to use and extend the wine scraper service.

## Quick Start

1. **Install dependencies using Make:**
   ```bash
   make install
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

3. **Run a test scrape:**
   ```bash
   make run-batch-test
   ```

4. **Find the results:** The scraped data will be saved in JSON files in the `./data/` directory.

## Detailed Usage

### Starting the RabbitMQ Service

The service processes winery messages from the `wineries_message` queue and publishes wine data to the `wines` exchange.

**Production mode (with RabbitMQ):**
```bash
python -m orchestration start
```

**Dry-run mode (no RabbitMQ):**
```bash
python -m orchestration start --dry-run
```

### Processing Wineries from File

To scrape wines from a list of wineries in a file:

**Example `test_wineries.txt`:**

```
https://www.weingut-rainer-sauer.de/,Weingut Rainer Sauer
https://www.buerklin-wolf.de/,Bürklin-Wolf
https://www.leitz-wein.de/,Weingut Leitz
```

**Production mode (publish to RabbitMQ):**
```bash
python -m orchestration process-file test_wineries.txt
```

**Dry-run mode (save to files):**
```bash
python -m orchestration process-file test_wineries.txt --dry-run
```

**Options:**
- `--dry-run`: Save results to JSON files instead of sending to RabbitMQ
- `--output-dir`: Directory for dry-run results (default: `./data`)

### Message Format

The service expects messages in the `wineries_message` queue with the following format:

```json
{
  "name": "Weingut Leitz",
  "website": "https://www.leitz-wein.de/"
}
```

Published wine data will be sent to the `wines` exchange with routing key `wine.scraped`.

### Queue Configuration

- **Input queue**: `wineries_message`
- **Output exchange**: `wines` (Topic exchange)
- **Routing key**: `wine.scraped`

## Adding a New Scraper

To add a new scraper for a new source, follow these steps:

1.  **Create a new scraper file:**

    Create a new Python file in the `scraperhub/scrapers/` directory (e.g., `new_source_scraper.py`).

2.  **Implement the scraper class:**

    Your new scraper class should inherit from `BaseScraper` and implement the `search` and `get_wine_details` methods.

    ```python
    # scraperhub/scrapers/new_source_scraper.py

    from .base import BaseScraper

    class NewSourceScraper(BaseScraper):
        def __init__(self):
            super().__init__("new_source", "https://www.new-source.com")

        async def search(self, query: str) -> list[dict]:
            # Implement search logic here
            pass

        async def get_wine_details(self, wine_id: str) -> dict:
            # Implement logic to get wine details here
            pass
    ```

3.  **Update `scrapers/__init__.py`:**

    Add your new scraper to the `__all__` list in `scraperhub/scrapers/__init__.py`.

4.  **Update `cli.py`:**

    In `scraperhub/cli.py`, update the `search` and `batch_search` commands to include your new scraper.

### Running the RabbitMQ Service

To start the service in RabbitMQ mode (production):

```bash
python cli.py service --rabbitmq-url amqp://rabbitmq:rabbitmq@localhost:5672/
```

To start in dry-run mode (no RabbitMQ):

```bash
python cli.py service --dry-run
```

### Using Make Commands

The project includes a Makefile with convenient commands:

- `make install`: Create venv and install dependencies
- `make run-service`: Start RabbitMQ service mode
- `make run-dry-run`: Start service in dry-run mode
- `make run-batch-test`: Test scraping with sample wineries
- `make run-single`: Test scraping a single winery
- `make clean`: Clean cache and temporary files
- `make lint`: Run code linting
- `make test`: Run basic tests

### Improving the Winery Scraper

The current implementation focuses on direct winery website scraping. To improve the winery scraper:

1. **Enhance wine detection:** Modify the `is_wine_url()` method in `scrapers/winery.py` to better identify actual wine product pages vs navigation pages.

2. **Add specific selectors:** Update the CSS selectors in `extract_wine_details()` to match the specific structure of target winery websites.

3. **Improve URL discovery:** Enhance the `discover_wine_urls()` method to better find wine product pages on different winery websites.

## Troubleshooting

- **Scraping is blocked or fails:** Websites may change their layout or implement anti-scraping measures. If a scraper is failing, you may need to update the selectors in the corresponding scraper file. Using the `--save-html` flag can help with debugging.

- **Dependencies are not installed:** Make sure you have installed all the required dependencies from `requirements.txt` in a virtual environment.

- **Playwright browser not found:** The first time you run the application, Playwright will download the necessary browser binaries. If this fails, you can try installing them manually:

  ```bash
  playwright install
  ```

- **Validation errors:** If you encounter Pydantic validation errors, check that your Wine model fields match the data being extracted.

## Cross-Language Type Sharing

### Generating Java DTOs from Python Models

The Wine model can be automatically converted to Java DTOs using JSON Schema:

#### 1. Generate JSON Schema

```bash
# From the scraperhub directory
python3 generate_schema_standalone.py
```

This creates `wine-schema.json` containing the complete JSON Schema for the Wine model.

#### 2. Generate Java DTOs

**Option A: Using jsonschema2pojo (Recommended)**

```bash
# Install jsonschema2pojo (requires Java)
brew install jsonschema2pojo

# Generate Java classes
jsonschema2pojo --source wine-schema.json \
    --target java-gen \
    --package com.wine.dto \
    --class-name Wine \
    --annotation-style jackson2
```

**Option B: Using Maven Plugin**

Add to your `pom.xml`:

```xml
<plugin>
    <groupId>org.jsonschema2pojo</groupId>
    <artifactId>jsonschema2pojo-maven-plugin</artifactId>
    <version>1.2.1</version>
    <configuration>
        <sourceDirectory>${basedir}/src/main/resources/schema</sourceDirectory>
        <targetPackage>com.wine.dto</targetPackage>
        <annotationStyle>jackson2</annotationStyle>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>generate</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**Option C: Manual Java Record**

```java
import java.util.List;
import java.util.Map;

public record Wine(
    String name,
    String winery_name,
    String winery_website,
    String type,
    String region,
    String country,
    List<String> grapes,
    Double alcohol_content,
    Integer vintage,
    Double price,
    String description,
    String quality_level,
    String shop_url,
    String bottle_size,
    Double average_rating,
    Integer number_of_ratings,
    Map<String, Double> critic_scores,
    List<String> food_pairings,
    String serving_temperature,
    String availability_status,
    String sku,
    String image_url,
    String scraped_at
) {}
```

#### 3. Usage Example

```python
# Python → JSON
from pipelines.models import Wine
wine = Wine(name="Riesling", winery_name="Leitz", winery_website="https://leitz.de")
json_data = wine.model_dump_json()
```

```java
// JSON → Java
ObjectMapper mapper = new ObjectMapper();
Wine wine = mapper.readValue(json_data, Wine.class);
```
