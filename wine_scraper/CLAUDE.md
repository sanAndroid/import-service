## CLAUDE.md - Instructions for Tomorrow

### Current Context:

- **Overall Project Goal:** The larger project aims to gather data about wines from winery websites to feed into a RAG (Retrieval-Augmented Generation) / MCP (Multi-Criteria Personalization) server. This showcases proficiency with different technologies.

- **Current Service Focus:** This specific service is a consumer of a RabbitMQ queue named `wineries`. Its primary responsibility is to read messages from this queue and then scrape the corresponding winery websites.

- **Input Message Format:** The messages received from the `wineries` RabbitMQ queue will be simplified. Each message will contain only two pieces of information:
    - `url`: The URL of the winery's website to be scraped.
    - `name`: The name of the winery.

### Information to Extract:

- The service should focus on extracting information about **wines on sale by the winery** from the provided `url`.
- Existing scrapers within this project (e.g., `vivino.py`, `wine_searcher.py`) can be used as a reference for implementing the scraping logic and data extraction patterns.
- For each wine found, the following specific data points (fields) should be extracted:
    1.  **Name**
    2.  **Winery Name**
    3.  **Vintage**
    4.  **Grape Varieties**
    5.  **Price**
    6.  **Description**
    7.  **Image URL**
    8.  **Region**
    9.  **Quality Level** (e.g., Großes Gewächs, Grand Cru, Ortswein, Gutswein)
    10. **URL in the Shop** (direct link to the wine's product page)
    11. **Wine Type** (e.g., Red, White, Rosé, Sparkling, Dessert)
    12. **Alcohol Content (ABV)**
    13. **Bottle Size**
    14. **Country**
    15. **Average Rating / Score**
    16. **Number of Ratings**
    17. **Critic Scores**
    18. **Food Pairings**
    19. **Serving Temperature**
    20. **Availability Status**
    21. **SKU/Product ID**

### Output Handling:

- In production, the scraped wine information should be sent to a RabbitMQ queue and exchange named `wines`.
- A `--dry-run` option should be available to write the extracted information directly to the terminal for debugging and development purposes.

### Technology Stack:

- **Python** with **Playwright** is the preferred choice for this scraping service, given its ability to handle complex websites with JavaScript.

### Error Handling:

- The service should be robust and not crash on errors encountered during website scraping. Errors should be logged, and the service should continue processing other wineries/wines.

### Service Trigger and Lifecycle:

- The service will be started from the command line.
- It will accept input in two ways:
    1.  By default, it will read winery URLs and names from the RabbitMQ `wineries` queue.
    2.  Alternatively, a list of winery URLs and names can be passed as a command-line parameter, in which case the RabbitMQ queue will not be used for input.
- Once all specified wineries (either from the queue or the command-line list) have been scraped, the service will terminate.