"""File-based data sinks for storing scraped data."""

import csv
import json
from pathlib import Path
from typing import List, Optional

import pandas as pd

from pipelines.models import Wine
from settings import settings


class CSVSink:
    """CSV file data sink."""

    def __init__(self, filename: Optional[str] = None):
        """Initialize CSV sink."""
        self.filename = filename or settings.csv_filename
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.output_dir / self.filename

    def save_wines(self, wines: List[Wine]) -> None:
        """Save wines to CSV file."""
        if not wines:
            return

        # Convert wines to dict format
        data = []
        for wine in wines:
            wine_dict = wine.dict()
            
            # Flatten ratings for CSV
            ratings_dict = {}
            for rating in wine_dict["ratings"]:
                source = rating["source"]
                ratings_dict[f"{source}_rating"] = rating["rating"]
                ratings_dict[f"{source}_count"] = rating["ratings_count"]
                ratings_dict[f"{source}_critics"] = rating["critics_rating"]
                ratings_dict[f"{source}_critics_count"] = rating["critics_count"]
            
            wine_dict.update(ratings_dict)
            wine_dict.pop("ratings", None)  # Remove nested ratings
            
            data.append(wine_dict)

        # Create DataFrame and save
        df = pd.DataFrame(data)
        
        # If file exists, append with header only if file is empty
        if self.filepath.exists():
            df.to_csv(self.filepath, mode="a", header=False, index=False)
        else:
            df.to_csv(self.filepath, index=False)

    def load_wines(self) -> List[Wine]:
        """Load wines from CSV file."""
        if not self.filepath.exists():
            return []

        try:
            df = pd.read_csv(self.filepath)
            
            # Convert DataFrame back to Wine objects
            wines = []
            for _, row in df.iterrows():
                wine_dict = row.to_dict()
                
                # Reconstruct ratings
                ratings = []
                sources = set()
                
                for col in wine_dict:
                    if col.endswith("_rating"):
                        source = col.replace("_rating", "")
                        sources.add(source)
                
                for source in sources:
                    rating = {
                        "source": source,
                        "rating": wine_dict.get(f"{source}_rating"),
                        "ratings_count": wine_dict.get(f"{source}_count"),
                        "critics_rating": wine_dict.get(f"{source}_critics"),
                        "critics_count": wine_dict.get(f"{source}_critics_count"),
                    }
                    # Remove None values
                    rating = {k: v for k, v in rating.items() if v is not None}
                    ratings.append(rating)
                
                wine_dict["ratings"] = ratings
                
                # Remove flattened rating columns
                for source in sources:
                    for suffix in ["_rating", "_count", "_critics", "_critics_count"]:
                        wine_dict.pop(f"{source}{suffix}", None)
                
                wines.append(Wine(**wine_dict))
            
            return wines
            
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return []


class JSONSink:
    """JSON file data sink."""

    def __init__(self, filename: str = "wines.json"):
        """Initialize JSON sink."""
        self.filename = filename
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.output_dir / self.filename

    def save_wines(self, wines: List[Wine]) -> None:
        """Save wines to JSON file."""
        if not wines:
            return

        # Convert to JSON-serializable format
        data = [wine.dict() for wine in wines]

        # If file exists, load existing data and append
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                data = existing_data + data
            except Exception:
                existing_data = []

        # Save to file
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_wines(self) -> List[Wine]:
        """Load wines from JSON file."""
        if not self.filepath.exists():
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            return [Wine(**item) for item in data]
            
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return []


class ParquetSink:
    """Parquet file data sink for efficient storage."""

    def __init__(self, filename: str = "wines.parquet"):
        """Initialize Parquet sink."""
        self.filename = filename
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.output_dir / self.filename

    def save_wines(self, wines: List[Wine]) -> None:
        """Save wines to Parquet file."""
        if not wines:
            return

        # Convert to DataFrame
        data = [wine.dict() for wine in wines]
        df = pd.DataFrame(data)
        
        # Save to Parquet
        if self.filepath.exists():
            existing_df = pd.read_parquet(self.filepath)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_parquet(self.filepath, index=False)

    def load_wines(self) -> List[Wine]:
        """Load wines from Parquet file."""
        if not self.filepath.exists():
            return []

        try:
            df = pd.read_parquet(self.filepath)
            
            # Convert DataFrame rows to Wine objects
            wines = []
            for _, row in df.iterrows():
                wine_dict = row.to_dict()
                wines.append(Wine(**wine_dict))
            
            return wines
            
        except Exception as e:
            print(f"Error loading Parquet: {e}")
            return []