import asyncio
import random
import re
from collections import deque
from pathlib import Path
from typing import List, Set, Tuple, Optional
from urllib.parse import urljoin, urlparse
import joblib

from playwright.async_api import Page
from utils.observability import get_logger
from config.settings import settings

logger = get_logger("scraper.discovery")

def tokenize_url(url: str) -> List[str]:
    """Tokenize URL parts into meaningful tokens for ML features."""
    parsed = urlparse(url)
    tokens: List[str] = []

    # Domain/netloc tokens (split on dots)
    if parsed.netloc:
        tokens.extend([t for t in parsed.netloc.lower().split('.') if t])

    # Path tokens (split on slashes/dashes/underscores)
    path = parsed.path or ""
    for part in path.lower().split('/'):
        if not part:
            continue
        # further split common slug formats
        for sub in re.split(r"[-_]+", part):
            if sub:
                tokens.append(sub)

    # Query tokens (include keys and generic markers)
    if parsed.query:
        tokens.append("has_query")
        for q in parsed.query.lower().split('&'):
            k = q.split('=')[0]
            if k:
                tokens.append(f"q_{k}")

    return tokens


def get_url_features(url: str) -> str:
    """Compose a feature string compatible with existing TF-IDF pipeline.

    Maintains backward-compatible numeric feature tokens and augments with
    URL text tokens that a retrained model can leverage.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parsed_url.query

    # Backward-compatible numeric tokens
    features = {
        "path_depth": path.count('/') or 0,
        "path_length": len(path) or 0,
        "query_params": len(query.split('&')) if query else 0,
        "has_html_extension": 1 if path.endswith(".html") else 0,
        "has_php_extension": 1 if path.endswith(".php") else 0,
    }
    numeric_tokens = [f"{k}_{v}" for k, v in features.items()]

    # Augmented text tokens (ignored by old model, used by retrained one)
    text_tokens = tokenize_url(url)

    return " ".join(numeric_tokens + text_tokens)

class UrlDiscoverer:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.original_base_url = base_url
        self.base_url = base_url
        # Robust model loading with fallback to heuristic
        self.model = None
        try:
            # Prefer repo-relative path
            model_path = Path(__file__).resolve().parent.parent / 'wine_url_classifier.joblib'
            if model_path.exists():
                self.model = joblib.load(model_path)
            else:
                # Fallback to CWD if user runs from project root
                self.model = joblib.load('wine_url_classifier.joblib')
            logger.info("URL classifier model loaded.")
        except Exception as e:
            logger.warning(f"URL classifier unavailable, using heuristic only: {e}")

    async def discover_wine_urls(self) -> List[str]:
        await self._find_and_set_shop_url()

        logger.info(f"Starting main crawl from {self.base_url}")
        all_urls = await self._crawl_site_for_links(self.base_url)

        wine_urls: List[str] = []
        for url in all_urls:
            if self._is_wine_product_page(url):
                wine_urls.append(url)
        
        return list(set(wine_urls))

    def _is_wine_product_page(self, url: str) -> bool:
        """Judge with ML proba and heuristic fallback.

        High-precision by default with configurable threshold.
        """
        features = get_url_features(url)
        # ML path
        try:
            if self.model is not None and hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba([features])[0]
                classes = list(self.model.classes_)
                if 'wine' in classes:
                    p_wine = float(proba[classes.index('wine')])
                else:
                    # Unknown label ordering; fallback to predicted label
                    pred = self.model.predict([features])[0]
                    p_wine = 1.0 if pred == 'wine' else 0.0

                if p_wine >= settings.url_classifier_threshold:
                    logger.debug(f"ML judge: ACCEPT {url} (p={p_wine:.2f})")
                    return True
                if p_wine <= 0.3:
                    logger.debug(f"ML judge: REJECT {url} (p={p_wine:.2f})")
                    return False
                # Uncertain → fall through to heuristic
                logger.debug(f"ML judge: UNCERTAIN {url} (p={p_wine:.2f}), using heuristic")
        except Exception as e:
            logger.debug(f"ML judge failure for {url}: {e}")

        # Heuristic fallback
        result = self._heuristic_is_product(url)
        logger.debug(f"Heuristic judge: {'ACCEPT' if result else 'REJECT'} {url}")
        return result

    def _heuristic_is_product(self, url: str) -> bool:
        u = url.lower()
        bad = [
            'impressum','datenschutz','privacy','agb','terms','versand','shipping',
            'kontakt','contact','about','ueber','ueber-uns','blog','news','events',
            'warenkorb','cart','checkout','kasse','login','account','sitemap','search','suche'
        ]
        if any(b in u for b in bad):
            return False
        good = [
            'produkt','product','detail','article','item','sku','buy','kaufen',
            '/weine','/wein','/shop','/store','/catalog','?id=','?number=','/p-','/prod-','/artikel'
        ]
        return any(g in u for g in good)

    async def _find_and_set_shop_url(self):
        logger.info("Phase 1: Searching for a shop entry point…")
        shop_url_found = False
        start_path_candidate: Optional[str] = None
        
        try:
            logger.info(f"Attempting to navigate to {self.original_base_url}")
            await self.page.goto(self.original_base_url, wait_until="domcontentloaded", timeout=30000)
            logger.info(f"Successfully navigated to {self.original_base_url}")
            links = await self.page.query_selector_all("a[href]")
            for link in links:
                href = await link.get_attribute('href')
                text = (await link.text_content()) or ''
                if href:
                    full_url = urljoin(self.original_base_url, href)
                    parsed = urlparse(full_url)
                    netloc = parsed.netloc.lower()
                    path = parsed.path.lower()
                    text_l = text.lower()
                    # Accept subdomain shop.*
                    if 'shop.' in netloc:
                        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
                        logger.info(f"Found shop subdomain: {self.base_url}. Switching base URL.")
                        shop_url_found = True
                        return
                    # Also accept common shop paths/texts
                    shop_markers = ['shop', 'store', 'weine', 'wein', 'produkt', 'produkte', 'catalog', 'onlineshop']
                    if any(m in path for m in ['/_shop','/shop','/store','/weine','/wein','/produkt','/produkte','/catalog']):
                        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
                        start_path_candidate = full_url
                    elif any(m in text_l for m in shop_markers):
                        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
                        start_path_candidate = full_url
        except Exception as e:
            logger.warning(f"Could not find shop link: {e}")

        if not shop_url_found:
            logger.info("No shop link found, attempting to guess subdomain.")
            parsed_base = urlparse(self.original_base_url)
            if parsed_base.netloc.startswith('www.'):
                guessed_domain = parsed_base.netloc.replace('www.', 'shop.')
            else:
                guessed_domain = f"shop.{parsed_base.netloc}"
            
            guessed_url = f"{parsed_base.scheme}://{guessed_domain}"
            
            try:
                response = await self.page.goto(guessed_url, wait_until="domcontentloaded")
                if response and response.ok:
                    logger.info(f"Guessed shop URL {guessed_url} is valid. Switching base URL.")
                    self.base_url = guessed_url
                else:
                    logger.info(f"Guessed shop URL is not valid.")
            except Exception as e:
                logger.info(f"Guessed shop URL failed to load: {e}")

        # If we found a good starting path within the same domain, set it for initial crawl
        if start_path_candidate:
            self.base_url = f"{urlparse(start_path_candidate).scheme}://{urlparse(start_path_candidate).netloc}"
            # Seed crawling from the identified shop/catalog path
            self._initial_crawl_url = start_path_candidate
        else:
            self._initial_crawl_url = self.base_url

    async def _crawl_site_for_links(self, start_url: str) -> Set[str]:
        visited_canon: Set[str] = set()
        to_visit: deque[Tuple[str, int]] = deque()
        # Start from the best-known entry (shop path if discovered)
        seed_url = getattr(self, '_initial_crawl_url', start_url)
        to_visit.append((seed_url, 0))
        all_links: Set[str] = set()

        max_depth = settings.scraper_max_crawl_depth
        max_urls = settings.scraper_max_urls_per_domain

        while to_visit and len(all_links) < max_urls:
            url, depth = to_visit.popleft()
            if depth > max_depth:
                continue
            parsed = urlparse(url)
            canon = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if canon in visited_canon:
                continue
            visited_canon.add(canon)
            
            try:
                await self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(random.uniform(0.3, 1.0))
                all_links.add(url)  # keep full URL with query for classification
                
                if depth < max_depth:
                    links = await self.page.query_selector_all("a[href]")
                    for link in links:
                        href = await link.get_attribute('href')
                        if href:
                            full_url = urljoin(self.base_url, href)
                            parsed_url = urlparse(full_url)
                            clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                            if self._is_internal_and_valid(clean_url) and clean_url not in visited_canon:
                                to_visit.append((full_url, depth + 1))
            except Exception as e:
                logger.warning(f"Failed to crawl {url}: {e}")
                continue
        return all_links

    def _is_internal_and_valid(self, url: str) -> bool:
        try:
            base_domain = urlparse(self.base_url).netloc.replace("www.","")
            url_domain = urlparse(url).netloc.replace("www.","")
            if not url_domain.endswith(base_domain):
                 return False
        except Exception:
            return False
        ignored_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.rar', '.mp3', '.mp4', '.docx', '.xlsx']
        if any(url.lower().endswith(ext) for ext in ignored_extensions):
            return False
        if url.startswith('mailto:') or url.startswith('tel:'):
            return False
        return True
