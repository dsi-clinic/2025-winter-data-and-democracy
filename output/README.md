# Election Data Output

This folder contains standardized election data CSV files that have been reformatted to follow a consistent format.

## File Format

Each CSV file follows a standard format with the following columns:

| Column Name | Description | Example |
|-------------|-------------|---------|
| STATE | State name (uppercase) | ALABAMA |
| YEAR | Election year | 1996 |
| RACE_TYPE | Type of election | House, Senate, Presidential |
| CONGRESSIONAL_DISTRICT | District number (if applicable) | 1 |
| CANDIDATE_NAME | Full name of the candidate | John Smith |
| CANDIDATE_PARTY | Political party affiliation | Republican, Democratic |
| VOTES | Number of votes received | 123456 |

## Data Consistency

All files maintain the following consistent formatting:
- State names are in uppercase (e.g., "OHIO" instead of "Ohio")
- Header row with standardized column names
- Consistent column ordering
- Preserved original case for race types, candidate names, and party affiliations

## Data Sources

These files contain reformatted versions of the original election data. The original source data was obtained from https://history.house.gov/Institution/Election-Statistics/Election-Statistics/

## Coverage

Files are named by election year (e.g., 1996.csv) and include data for:
- Congressional elections (House and Senate races)
- Presidential elections

## Usage Notes

- All vote counts are provided as reported by the original sources
- Empty cells in the original data are preserved as empty fields
- Congressional districts are represented as numbers, with blank values for statewide races
- Party affiliations match those reported in the original data sources
- Write-in candidates are designated as "Write-in" in the party field when applicable

## Last Updated

March 12, 2025
