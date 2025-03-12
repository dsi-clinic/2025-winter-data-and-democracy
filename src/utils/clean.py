"""This module provides functionality to process CSV files in batch.

It reads CSV files, cleans their data, sorts them by specified columns,
and saves the cleaned files to a designated output folder.

Features:
- Cleans column names by stripping whitespace.
- Normalizes column names to uppercase for consistency.
- Skips files with a specified prefix.
- Handles missing or corrupt values gracefully.
- Sorts files based on provided columns, if possible.
"""

from pathlib import Path

import pandas as pd


def process_csv_files(
    input_folder: Path | None = None,
    output_folder: Path | None = None,
    sort_columns: list[str] = None,
    skip_prefix: str = "sorted_",
) -> tuple[list[str], list[str]]:
    """Batch process CSV files with optional sorting and cleaning.

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
        - Normalizes column names to uppercase for consistency
        - Preserves all data even if sorting columns aren't present
        - Skips files starting with skip_prefix
    """
    # Initialize sort_columns as empty list if None
    if sort_columns is None:
        sort_columns = []

    # Set default paths based on project structure
    project_root = Path(__file__).resolve().parent.parent.parent

    if input_folder is None:
        input_path = project_root / "data" / "csv"
    else:
        input_path = Path(input_folder)

    if output_folder is None:
        output_path = project_root / "output" / "csv"
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
            dataframe = pd.read_csv(file_path, engine="python", on_bad_lines="skip")

            # Clean and standardize column names
            dataframe.columns = dataframe.columns.str.strip().str.upper()

            # Check for header rows in data (common issue in some CSV files)
            # If first row seems to contain column headers, drop it
            first_row = dataframe.iloc[0]
            if any(
                str(val).upper() in [col.upper() for col in dataframe.columns]
                for val in first_row
            ):
                print(
                    f"Possible header row found in data for {filename}, removing first row"
                )
                dataframe = dataframe.iloc[1:].reset_index(drop=True)

            # Ensure VOTES column is converted to numeric
            if "VOTES" in dataframe.columns:
                dataframe["VOTES"] = (
                    pd.to_numeric(
                        dataframe["VOTES"]
                        .astype(str)
                        .str.replace(r"[^\d]", "", regex=True),
                        errors="coerce",
                    )
                    .fillna(0)
                    .astype(int)
                )

            # Map common column name variations
            column_mapping = {
                "YEARS": "YEAR",
                "YEAR_OF_ELECTION": "YEAR",
                "ELECTION_YEAR": "YEAR",
            }

            # Rename columns if variations exist
            for old_col, new_col in column_mapping.items():
                if old_col in dataframe.columns and new_col not in dataframe.columns:
                    dataframe.rename(columns={old_col: new_col})

            # Convert other relevant columns to appropriate types with better error handling
            type_conversions = {
                "YEAR": int,
                "CONGRESSIONAL_DISTRICT": str,
            }

            for col, dtype in type_conversions.items():
                if col in dataframe.columns:
                    try:
                        # For numeric conversions, handle non-numeric values safely
                        if isinstance(dtype, int):
                            # Check for non-numeric values and report them
                            non_numeric = ~dataframe[col].astype(str).str.replace(
                                r"\D", "", regex=True
                            ).str.match(r"^\d*$")
                            if non_numeric.any():
                                problematic_values = dataframe.loc[
                                    non_numeric, col
                                ].unique()
                                print(
                                    f"Warning: Non-numeric values found in {col} column: {problematic_values}"
                                )

                                # Replace non-numeric values with NaN
                                dataframe.loc[non_numeric, col] = pd.NA

                            # Convert to numeric and fill NaN values
                            dataframe[col] = pd.to_numeric(
                                dataframe[col], errors="coerce"
                            )

                            # For YEAR column, infer from filename if not available
                            if col == "YEAR" and dataframe[col].isna().any():
                                try:
                                    year_from_filename = int(filename.split(".")[0])
                                    MIN_YEAR = 1900
                                    MAX_YEAR = 2100
                                    if (
                                        MIN_YEAR <= year_from_filename <= MAX_YEAR
                                    ):  # Sanity check for valid year
                                        print(
                                            f"Inferring missing YEAR values from filename: {year_from_filename}"
                                        )
                                        dataframe[col] = dataframe[col].fillna(
                                            year_from_filename
                                        )
                                except (ValueError, IndexError):
                                    pass

                            # Fill remaining NaN values with a default
                            if col == "YEAR":
                                # Use median year if available, otherwise default to 0
                                median_year = dataframe[col].median()
                                default_value = (
                                    median_year if not pd.isna(median_year) else 0
                                )
                                dataframe[col] = (
                                    dataframe[col].fillna(default_value).astype(dtype)
                                )
                        else:
                            dataframe[col] = dataframe[col].astype(dtype)
                    except Exception as type_error:
                        print(
                            f"Warning: Could not convert column {col} to {dtype.__name__} in {filename}: {type_error}"
                        )
                        # Continue processing without stopping for type conversion errors

            # Sort if possible
            sort_cols_present = [
                col for col in sort_columns if col in dataframe.columns
            ]
            if sort_cols_present:
                dataframe = dataframe.sort_values(by=sort_cols_present)
                if len(sort_cols_present) < len(sort_columns):
                    missing_cols = set(sort_columns) - set(sort_cols_present)
                    print(
                        f"Warning: Missing sort columns in {filename}: {missing_cols}"
                    )

            # Save processed file
            dataframe.to_csv(output_file, index=False)
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
        print(f"Failed files: {', '.join(failed_files)}")

    return processed_files, failed_files


if __name__ == "__main__":
    # Process CSV files from the extracted_data directory
    process_csv_files()
