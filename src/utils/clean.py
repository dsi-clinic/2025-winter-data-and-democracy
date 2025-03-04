import pandas as pd
from pathlib import Path
from typing import Optional, List, Tuple

def process_csv_files(
    input_folder: Optional[str] = None,
    output_folder: Optional[str] = None,
    sort_columns: List[str] = ["STATE", "CONGRESSIONAL_DISTRICT"],
    skip_prefix: str = "sorted_"
) -> Tuple[List[str], List[str]]:
    """
    Batch process CSV files with optional sorting and cleaning.
    
    Args:
        input_folder: Path to folder containing input CSV files (defaults to data/csv)
        output_folder: Path to folder for processed output files (defaults to data/csv)
        sort_columns: List of columns to sort by (if present in CSV)
        skip_prefix: Prefix of files to skip processing
    
    Returns:
        Tuple[List[str], List[str]]: Lists of (successfully processed files, failed files)
    
    Raises:
        FileNotFoundError: If input_folder doesn't exist
        PermissionError: If cannot create output_folder
        
    Notes:
        - Creates output_folder if it doesn't exist
        - Cleans column names by stripping whitespace
        - Preserves all data even if sorting columns aren't present
        - Skips files starting with skip_prefix
    """
    # Set default paths based on project structure
    project_root = Path(__file__).resolve().parent.parent.parent
    
    if input_folder is None:
        input_path = project_root / "data" / "csv"
    else:
        input_path = Path(input_folder)
    
    if output_folder is None:
        output_path = project_root / "data" / "csv"
    else:
        output_path = Path(output_folder)
    
    # Validate input folder
    if not input_path.exists():
        raise FileNotFoundError(f"Input folder not found: {input_path}")
    if not input_path.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_path}")
        
    # Create output folder
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise PermissionError(f"Cannot create output directory: {output_path}") from e
        
    processed_files = []
    failed_files = []
    
    # Process each CSV file
    for file_path in input_path.glob("*.csv"):
        filename = file_path.name
        
        # Skip files with specified prefix
        if filename.startswith(skip_prefix):
            continue
            
        output_file = output_path / f"sorted_{filename}"
        
        try:
            # Read CSV with flexible parsing
            df = pd.read_csv(
                file_path,
                engine='python',
                on_bad_lines='skip'
            )
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Sort if possible
            if all(col in df.columns for col in sort_columns):
                df = df.sort_values(by=sort_columns)
            
            # Save processed file
            df.to_csv(output_file, index=False)
            processed_files.append(filename)
            print(f"Processed: {filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            failed_files.append(filename)
            continue
    
    # Provide summary
    if processed_files:
        print(f"\nSuccessfully processed {len(processed_files)} files")
    if failed_files:
        print(f"Failed to process {len(failed_files)} files")
    
    return processed_files, failed_files

if __name__ == "__main__":
    # Process CSV files from the extracted_data directory
    process_csv_files()
