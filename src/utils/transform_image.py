import os
from pathlib import Path
from typing import Optional, List, Dict
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError, PDFSyntaxError

def pdf_to_images(
    pdf_path: str,
    output_base: Optional[str] = None,
    dpi: int = 300,
    image_format: str = "PNG"
) -> List[Path]:
    """
    Convert a PDF file to a series of images.
    
    Args:
        pdf_path: Path to the input PDF file
        output_base: Base directory for output images (defaults to data/processed_images)
        dpi: Resolution of output images in dots per inch
        image_format: Format to save images (e.g., 'PNG', 'JPEG')
    
    Returns:
        List[Path]: List of paths to the generated image files
    
    Raises:
        FileNotFoundError: If PDF file or output directory doesn't exist/can't be created
        PermissionError: If lacking permissions to read PDF or write images
        PDFPageCountError: If PDF is empty or corrupted
        PDFSyntaxError: If PDF file is invalid
        ValueError: If invalid parameters are provided
        
    Notes:
        - Creates a subdirectory named after the PDF file
        - Images are named sequentially as page_1.png, page_2.png, etc.
        - Existing files will be overwritten
    """
    # Input validation
    if not isinstance(dpi, int) or dpi <= 0:
        raise ValueError(f"Invalid DPI value: {dpi}")
    if not image_format.upper() in ['PNG', 'JPEG', 'TIFF']:
        raise ValueError(f"Unsupported image format: {image_format}")
    
    # Set default output base directory if not specified
    if output_base is None:
        # Get project root directory (3 levels up from this file in src/utils)
        project_root = Path(__file__).resolve().parent.parent.parent
        output_base = project_root / "data" / "images"
    
    # Convert paths to Path objects for better handling
    pdf_path = Path(pdf_path)
    output_base = Path(output_base)
    
    # Validate input file
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if not pdf_path.is_file():
        raise ValueError(f"Not a file: {pdf_path}")
    
    # Create output directory
    pdf_name = pdf_path.stem
    output_folder = output_base / pdf_name
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise PermissionError(f"Cannot create output directory: {output_folder}") from e
    
    # Convert PDF to images
    try:
        images = convert_from_path(str(pdf_path), dpi=dpi)
    except (PDFPageCountError, PDFSyntaxError) as e:
        raise type(e)(f"Error processing PDF {pdf_path}: {str(e)}") from e
    
    # Save images
    saved_paths = []
    for i, image in enumerate(images, start=1):
        image_path = output_folder / f"page_{i}.{image_format.lower()}"
        try:
            image.save(str(image_path), image_format)
            saved_paths.append(image_path)
        except Exception as e:
            raise IOError(f"Failed to save image {image_path}: {str(e)}") from e
    
    if not saved_paths:
        raise PDFPageCountError(f"No images were generated from {pdf_path}")
    
    return saved_paths

def convert_all_pdfs(
    input_dir: Optional[str] = None, 
    output_dir: Optional[str] = None,
    dpi: int = 300,
    image_format: str = "PNG"
) -> dict:
    """
    Convert all PDFs in the input directory to images.
    
    Args:
        input_dir: Directory containing PDF files (defaults to data/scraped_pdfs)
        output_dir: Base directory for output images (defaults to data/images)
        dpi: Resolution of output images in dots per inch
        image_format: Format to save images
        
    Returns:
        dict: Dictionary mapping PDF filenames to lists of generated image paths
    """
    # Get project root directory (3 levels up from this file in src/utils)
    project_root = Path(__file__).resolve().parent.parent.parent
    
    # Set default directories if not specified
    if input_dir is None:
        input_dir = project_root / "data" / "scraped_pdfs"
    else:
        input_dir = Path(input_dir)
        
    if output_dir is None:
        output_dir = project_root / "data" / "images"
    else:
        output_dir = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Track results
    results = {}
    
    # Process each PDF in the input directory
    for pdf_file in input_dir.glob("*.pdf"):
        try:
            image_paths = pdf_to_images(
                pdf_path=str(pdf_file),
                output_base=str(output_dir),
                dpi=dpi,
                image_format=image_format
            )
            results[pdf_file.name] = image_paths
            print(f"Successfully processed {pdf_file.name}")
            print(f"Generated {len(image_paths)} images")
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
            results[pdf_file.name] = []
    
    return results

if __name__ == "__main__":
    # Process all PDFs from the scraped_pdfs directory
    convert_all_pdfs()
