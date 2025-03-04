import os
import base64
import re
from pathlib import Path
from typing import Optional, Dict, List
import anthropic

from prompts import SYSTEM_PROMPT, USER_PROMPT, get_custom_prompt

def extract_election_data(
    input_base: Optional[str] = None,
    output_base: Optional[str] = None,
    anthropic_api_key: Optional[str] = None,
    model_name: str = "claude-3-5-sonnet-20241022"
) -> Dict[str, Path]:
    """
    Extract election data from image files using Anthropic's Claude API.
    
    Args:
        input_base: Base directory containing image folders (defaults to data/images)
        output_base: Directory for output CSV files (defaults to data/csv)
        anthropic_api_key: Optional Anthropic API key (if not provided, uses environment variable)
        model_name: Anthropic model to use for image analysis
    
    Returns:
        Dict[str, Path]: Dictionary mapping folder names to their output CSV paths
    
    Raises:
        ValueError: If the API key is not provided and not found in environment
        FileNotFoundError: If input directory doesn't exist
        PermissionError: If lacking permissions to read/write files
    """
    # Set up default paths based on project structure
    project_root = Path(__file__).resolve().parent.parent.parent
    
    if input_base is None:
        input_base = project_root / "data" / "images"
    else:
        input_base = Path(input_base)
    
    if output_base is None:
        output_base = project_root / "data" / "csv"
    else:
        output_base = Path(output_base)
    
    # Create output directory if it doesn't exist
    output_base.mkdir(parents=True, exist_ok=True)
    
    # Initialize Anthropic client
    if anthropic_api_key:
        client = anthropic.Anthropic(api_key=anthropic_api_key)
    else:
        try:
            client = anthropic.Anthropic()
        except Exception as e:
            raise ValueError(f"Failed to initialize Anthropic client: {e}. Please provide an API key.")
    
    # Validate input directory
    if not input_base.exists():
        raise FileNotFoundError(f"Input directory not found: {input_base}")
    if not input_base.is_dir():
        raise ValueError(f"Not a directory: {input_base}")
    
    # Track results
    results = {}
    
    # Process each folder (each folder corresponds to a PDF)
    for folder_path in input_base.iterdir():
        if not folder_path.is_dir():
            continue
        
        folder_name = folder_path.name
        output_file = output_base / f"{folder_name}.csv"
        
        # Initialize CSV file with headers
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write("STATE,YEAR,RACE_TYPE,CONGRESSIONAL_DISTRICT,CANDIDATE_NAME,CANDIDATE_PARTY,VOTES\n")
        except PermissionError as e:
            raise PermissionError(f"Cannot create output file: {output_file}") from e
        
        # Determine if we can extract year from folder name for custom prompt
        year_match = re.search(r'(\d{4})', folder_name)
        year = year_match.group(1) if year_match else None
        
        # Process each image in the folder
        for image_file in sorted(folder_path.glob("*.png")):
            try:
                # Read and encode the image
                with open(image_file, "rb") as img:
                    image_data = base64.b64encode(img.read()).decode("utf-8")
                
                # Create a customized prompt if year is available
                user_prompt = get_custom_prompt(year=year) if year else USER_PROMPT
                
                # Send to Anthropic API
                response = client.messages.create(
                    model=model_name,
                    max_tokens=2048,
                    temperature=0,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": image_data,
                                    },
                                },
                                {
                                    "type": "text",
                                    "text": user_prompt
                                }
                            ],
                        }
                    ],
                )
                
                # Extract text from response
                response_text = None
                for block in response.content:
                    if block.type == "text":
                        response_text = block.text.strip()
                        break
                
                if response_text is None:
                    print(f"Failed to find valid text content for {image_file.name}.")
                    continue
                
                # Append to CSV file
                with open(output_file, "a", encoding="utf-8") as file:
                    file.write(response_text + "\n")
                
                print(f"Processed {image_file.name} into {output_file.name}")
                
            except Exception as e:
                print(f"Error processing {image_file.name}: {e}")
                continue
        
        results[folder_name] = output_file
    
    if not results:
        print("No folders were processed. Check your input directory structure.")
    else:
        print(f"Successfully processed {len(results)} folders")
    
    return results

if __name__ == "__main__":
    # Run the extraction standalone
    extract_election_data()
