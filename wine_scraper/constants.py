"""Constants used throughout the scraperhub."""

from pathlib import Path

# Directory paths
SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent.parent
DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = ROOT_DIR / ".cache"
TESTS_DIR = ROOT_DIR / "tests"

# HTTP constants
DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
}

# Wine sites
WINE_SITES = {
    "vivino": {
        "name": "Vivino",
        "base_url": "https://www.vivino.com",
        "search_path": "/search/wines",
    },
    "wine_searcher": {
        "name": "Wine-Searcher",
        "base_url": "https://www.wine-searcher.com",
        "search_path": "/find",
    },
    "tbsg": {
        "name": "TBSG",
        "base_url": "https://www.tbsg.de",
        "search_path": "/wein",
    },
}

# CSV column names
WINE_CSV_COLUMNS = [
    "name",
    "type",
    "image_link",
    "price",
    "vivino_rating",
    "vivino_ratings_count",
    "vivino_winery",
    "vivino_wine_name",
    "ws_user_rating",
    "ws_user_count",
    "ws_critics_rating",
    "ws_critics_count",
    "ws_wine_name",
]

# Retry configuration
RETRY_CONFIG = {
    "stop": "stop_after_attempt",
    "wait": "wait_exponential",
    "multiplier": 1,
    "min": 4,
    "max": 60,
}