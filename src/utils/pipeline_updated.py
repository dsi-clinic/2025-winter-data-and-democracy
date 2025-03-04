import os
import argparse
from pathlib import Path
from typing import Optional, Dict, List, Any

# Import all pipeline components
from scrape import scrape_pdfs
from transform_image import convert_all_pdfs
from transform_csv import extract_election_data
from clean import process_csv_files

def process_pipeline(
    scrape_url: Optional[str] = None,
    pdf_input_dir: Optional[str] = None,
    image_output_dir: Optional[str] = None,
    csv_output_dir: Optional[str] = None,
    anthropic_api_key: Optional[str] = None,
    dpi: int = 300,
    image_format: str = "PNG",
    skip_pdf_scraping: bool = False,
    skip_pdf_processing: bool = False,
    skip_image_processing: bool = False,
    skip_csv_processing: bool = False
) -> Dict[str, Any]:
    """
    Run the complete pipeline from scraping to data extraction.
    
    Args:
        scrape_url: URL to scrape for PDFs
        pdf_input_dir: Directory containing PDF files
        image_output_dir: Directory for output images
        csv_output_dir: Directory for extracted CSV data
        anthropic_api_key: Anthropic API key for image analysis
        dpi: Resolution of output images in dots per inch
        image_format: Format to save images
        skip_pdf_scraping: Skip the PDF scraping step
        skip_pdf_processing: Skip the PDF to image processing step
        skip_image_processing: Skip the image to CSV processing step
        skip_csv_processing: Skip the CSV processing step
        
    Returns:
        Dict[str, Any]: Results of the pipeline execution
    """
    # Set default URL if none provided
    if scrape_url is None and not skip_pdf_scraping:
        scrape_url = "https://history.house.gov/Institution/Election-Statistics/Election-Statistics/"
    
    # Set default paths based on project structure
    project_root = Path(__file__).resolve().parent.parent.parent
    
    if pdf_input_dir is None:
        pdf_input_dir = project_root / "data" / "scraped_pdfs"
    
    if image_output_dir is None:
        image_output_dir = project_root / "data" / "images"
        
    if csv_output_dir is None:
        csv_output_dir = project_root / "data" / "csv"
    
    # Create necessary directories
    for directory in [pdf_input_dir, image_output_dir, csv_output_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    # Step 1: Scrape PDFs if not skipped
    if not skip_pdf_scraping:
        print(f"Step 1: Scraping PDFs from {scrape_url}")
        scrape_pdfs(scrape_url)
    else:
        print("Step 1: Skipping PDF scraping")
    
    # Step 2: Convert PDFs to images if not skipped
    if not skip_pdf_processing:
        print("Step 2: Converting PDFs to images")
        image_results = convert_all_pdfs(
            input_dir=str(pdf_input_dir),
            output_dir=str(image_output_dir),
            dpi=dpi,
            image_format=image_format
        )
        results["images"] = image_results
    else:
        print("Step 2: Skipping PDF to image conversion")
    
    # Step 3: Extract data from images if not skipped
    if not skip_image_processing:
        print("Step 3: Extracting election data from images")
        csv_results = extract_election_data(
            input_base=str(image_output_dir),
            output_base=str(csv_output_dir),
            anthropic_api_key=anthropic_api_key
        )
        results["csv_files"] = csv_results
    else:
        print("Step 3: Skipping image to CSV extraction")
    
    # Step 4: Process CSV files if not skipped
    if not skip_csv_processing:
        print("Step 4: Processing and sorting CSV files")
        csv_processing_results = process_csv_files(
            input_folder=str(csv_output_dir),
            output_folder=str(csv_output_dir)
        )
        results["processed_csv"] = csv_processing_results
    else:
        print("Step 4: Skipping CSV processing")
    
    print("Pipeline execution completed!")
    return results

def main():
    """Parse command line arguments and run the pipeline."""
    parser = argparse.ArgumentParser(description="Process election data pipeline")
    
    # Pipeline control arguments
    parser.add_argument("--skip-scraping", action="store_true", help="Skip PDF scraping step")
    parser.add_argument("--skip-pdf-processing", action="store_true", help="Skip PDF to image conversion step")
    parser.add_argument("--skip-image-processing", action="store_true", help="Skip image to CSV extraction step")
    parser.add_argument("--skip-csv-processing", action="store_true", help="Skip CSV processing step")
    
    # Configuration arguments
    parser.add_argument("--scrape-url", help="URL to scrape PDFs from")
    parser.add_argument("--anthropic-api-key", help="Anthropic API key")
    parser.add_argument("--dpi", type=int, help="Image resolution in DPI")
    parser.add_argument("--image-format", choices=["PNG", "JPEG", "TIFF"], help="Image format")
    
    args = parser.parse_args()
    
    # Run pipeline with command line arguments
    process_pipeline(
        scrape_url=args.scrape_url,
        anthropic_api_key=args.anthropic_api_key,
        dpi=args.dpi,
        image_format=args.image_format,
        skip_pdf_scraping=args.skip_scraping,
        skip_pdf_processing=args.skip_pdf_processing,
        skip_image_processing=args.skip_image_processing,
        skip_csv_processing=args.skip_csv_processing
    )

if __name__ == "__main__":
    # Run the full pipeline with default settings
    process_pipeline()
