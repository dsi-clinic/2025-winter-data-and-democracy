

# Data Folder Documentation

## Election Data PDF Files

This folder is intended to store election data PDF files retrieved from the U.S. House of Representatives' Office of the Clerk historical election statistics page.

## How to Retrieve the Data

The election PDF files can be downloaded automatically using the `scrape.py` utility script located in the `src/utils` directory. This script uses Selenium and Requests to fetch PDF files from the official U.S. House of Representatives website.

### Data Source

All election data is sourced from the official U.S. House of Representatives' Office of the Clerk:
[https://history.house.gov/Institution/Election-Statistics/Election-Statistics/](https://history.house.gov/Institution/Election-Statistics/Election-Statistics/)

### Running the Scraper

To download the election data PDFs, run the following command from the project root:

```bash
python src/utils/scrape.py
```

The script will:
1. Launch a headless Chrome browser to navigate to the election statistics page
2. Find all PDF links in the table rows on the page
3. Extract the election year from each URL
4. Download each PDF with a filename based on its year
5. Save the files to the directory specified in the config module as `PDF_DIR`

### Requirements

The scraper requires Python with the following dependencies:
- requests
- selenium
- Chrome WebDriver

You can install the Python dependencies with:
```bash
pip install -r requirements.txt
```

You'll also need to have Chrome browser installed and the appropriate ChromeDriver for your Chrome version.

## Script Configuration

The script uses configuration values imported from a `config` module:
- `PDF_DIR`: Path to the directory where PDFs will be saved
- `SCRAPE_URL`: The URL to scrape (default is the House election statistics page)

## Notes

- The script automatically handles duplicate filenames by appending a counter
- If a PDF link doesn't contain a year in the format `/YYYY/`, it will be saved as "unnamed_file.pdf"
- The script outputs status messages to the console during the download process
- Failed downloads will be reported but won't stop the script from processing other files
