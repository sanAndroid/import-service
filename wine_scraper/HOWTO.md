# How-To Guide

This guide provides detailed instructions on how to use and extend the `scraperhub` tool.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run a search:**
   ```bash
   python -m scraperhub.cli search "Chateau Lafite Rothschild"
   ```

3. **Find the results:** The scraped data will be saved in the `data/` directory by default.

## Detailed Usage

### Performing a Single Wine Search

To search for a single wine, use the `search` command. You must provide a search query.

```bash
python -m scraperhub.cli search "Opus One"
```

**Options:**

- `--source` or `-s`: Specify the source to scrape from (`vivino`, `wine_searcher`, or `all`). Defaults to `all`.
- `--output` or `-o`: Specify the output format (`csv`, `json`, or `both`). Defaults to `csv`.
- `--limit` or `-l`: The maximum number of results to return per source. Defaults to 5.
- `--save-html`: Save the HTML of the search results page for debugging.

**Example:**

```bash
python -m scraperhub.cli search "Opus One" --source vivino --output json --limit 3
```

### Performing a Batch Search

To search for multiple wines from a file, use the `batch-search` command. You need to provide a path to a text file containing one wine name per line.

**Example `wines.txt`:**

```
Dominus Estate
Harlan Estate
Sine Qua Non
```

**Command:**

```bash
python -m scraperhub.cli batch-search wines.txt
```

**Options:**

- `--source` or `-s`: The source to scrape from. Defaults to `all`.
- `--output` or `-o`: The output format. Defaults to `csv`.
- `--limit` or `-l`: The maximum number of results per query per source. Defaults to 3.

### Listing Available Sources

To see a list of all available scraping sources, use the `list-sources` command.

```bash
python -m scraperhub.cli list-sources
```

### Clearing the Cache

To clear all cached data, use the `clean-cache` command.

```bash
python -m scraperhub.cli clean-cache
```

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

## Troubleshooting

- **Scraping is blocked or fails:** Websites may change their layout or implement anti-scraping measures. If a scraper is failing, you may need to update the selectors in the corresponding scraper file. Using the `--save-html` flag can help with debugging.

- **Dependencies are not installed:** Make sure you have installed all the required dependencies from `requirements.txt` in a virtual environment.

- **Playwright browser not found:** The first time you run the application, Playwright will download the necessary browser binaries. If this fails, you can try installing them manually:

  ```bash
  playwright install
  ```

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
    String winery,
    String wineryWebsite,
    String type,
    String region,
    String country,
    List<String> grapes,
    Double alcoholContent,
    Integer vintage,
    Double price,
    String description,
    String qualityLevel,
    String shopUrl,
    String bottleSize,
    Double averageRating,
    Integer numberOfRatings,
    Map<String, Double> criticScores,
    List<String> foodPairings,
    String servingTemperature,
    String availabilityStatus,
    String sku,
    String imageUrl,
    String scrapedAt
) {}
```

#### 3. Usage Example

```python
# Python → JSON
from pipelines.models import Wine
wine = Wine(name="Riesling", winery="Leitz", winery_website="https://leitz.de")
json_data = wine.model_dump_json()
```

```java
// JSON → Java
ObjectMapper mapper = new ObjectMapper();
Wine wine = mapper.readValue(json_data, Wine.class);
```
