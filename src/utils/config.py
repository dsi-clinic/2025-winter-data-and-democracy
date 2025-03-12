"""Configuration settings for the election data processing pipeline.

This module defines paths, constants, and configuration settings used throughout
the application. It handles environment variables, directory structures, and
default configurations for various components of the pipeline.
"""

import os
from pathlib import Path

# Try to load from .env file if dotenv is installed
try:
    from dotenv import load_dotenv

    # Load environment variables from .env file if it exists
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    # python-dotenv not installed, continue without it
    pass

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Directory structure
DATA_DIR = PROJECT_ROOT / "data"
PDF_DIR = DATA_DIR / "scraped_pdfs"
IMAGE_DIR = DATA_DIR / "images"
CSV_DIR = DATA_DIR / "csv"

# Create directories if they don't exist
for directory in [DATA_DIR, PDF_DIR, IMAGE_DIR, CSV_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Claude API settings - get API key from environment variable
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# URL for scraping
SCRAPE_URL = (
    "https://history.house.gov/Institution/Election-Statistics/Election-Statistics/"
)

# Claude configuration
CLAUDE_CONFIG = {
    "model_name": "claude-3-5-sonnet-20241022",
    "max_tokens": 2048,
    "temperature": 0,
}

# PDF processing settings
PDF_CONFIG = {"dpi": 300, "image_format": "PNG"}

# CSV processing settings
CSV_CONFIG = {
    "sort_columns": ["STATE", "CONGRESSIONAL_DISTRICT"],
    "skip_prefix": "sorted_",
}


def main():
    """Setup function that ensures directories exist and environment is properly functioning"""
    # Ensure directoires exist
    for directory in (DATA_DIR, PDF_DIR, IMAGE_DIR, CSV_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    # Return True if everything is set up correctly
    return True


if __name__ == "__main__":
    main()
