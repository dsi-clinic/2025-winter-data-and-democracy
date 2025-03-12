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

## PDF Image Extraction
In addition to storing the raw PDF files, this folder will also contain images of each PDF page when the `transform_image.py` script is run.

### Running the Image Transformer
To extract images from the downloaded PDFs, run the following command from the project root:
```bash
python src/utils/transform_image.py
```

The script will:
1. Process each PDF in the `PDF_DIR` directory
2. Convert each page to a high-resolution image
3. Save the images in the same directory with naming convention `{year}_page_{page_number}.jpg`
4. These images are used for OCR processing in later pipeline stages

## Testing Data
This folder also contains testing data used for accuracy statistics and validation in example_outputs:

- A subset of manually annotated election data pages
- Ground truth CSV files for comparing OCR results
- Accuracy benchmark files that track extraction performance

The testing data is used by the evaluation scripts to generate metrics on:
- String Variables: Levenshtein Distance
- Numerical Variables: Custom Digit-Level Accuracy Measurement
- Confusion Matrix
- Additional Error Measurements: Absolute + Percentage Error, Plot of Error Distribution

These metrics are reported during pipeline validation and can be accessed through the project's test reports.

## Notes
- The script automatically handles duplicate filenames by appending a counter
- If a PDF link doesn't contain a year in the format `/YYYY/`, it will be saved as "unnamed_file.pdf"
- The script outputs status messages to the console during the download process
- Failed downloads will be reported but won't stop the script from processing other files
- Image files can be quite large; ensure you have sufficient disk space before running `transform_image.py`
- The testing data should not be modified manually as it serves as a benchmark for accuracy evaluation
