# Utils Directory

This directory contains utility modules for the election data processing pipeline.

## Contents

- `config.py`: Central configuration file with settings for all pipeline components
- `pipeline.py`: Main pipeline coordination script
- `scrape.py`: Module for scraping PDF files from the House website
- `transform_image.py`: Module for converting PDF files to images
- `transform_csv.py`: Module for extracting election data from images using Claude
- `clean.py`: Module for processing and sorting CSV files
- `prompts.py`: Module containing Claude API prompts for data extraction

Each module can be run independently or as part of the full pipeline.

## Environment Setup

This application requires an Anthropic API key. Before running the Docker container, set the ANTHROPIC_API_KEY environment variable:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
