from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import os
import re
from typing import List
from urllib.parse import urlparse

def scrape_pdfs(url: str) -> None:
    """
    Scrapes PDF links from a given website and downloads them to a local directory.
    
    Args:
        url (str): The URL of the website to scrape PDFs from.
    
    Raises:
        ValueError: If the URL provided is not a valid string.
    """
    if not isinstance(url, str) or not url.startswith("http"):
        raise ValueError("Invalid URL provided. Please enter a valid URL.")
    
    # Set up Chrome options
    download_dir = "./data/election_pdfs"
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = '/usr/bin/google-chrome'
    # chrome_options.add_experimental_option("prefs", {
    #     "download.default_directory": download_dir,
    #     "download.prompt_for_download": False,
    #     "download.directory_upgrade": True,
    #     "plugins.always_open_pdf_externally": True
    # })
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # Find all the table rows
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    pdf_links = []
    
    for row in rows[1:]:  # Skip the header row
        cells = row.find_elements(By.TAG_NAME, "td")
        for cell in cells:
            link = cell.find_element(By.TAG_NAME, "a")
            href = link.get_attribute("href")
            print(href)
            pdf_links.append(href)
    
    # Close the browser
    driver.quit()
    
    for link in pdf_links:
        # Extract the year from the URL using regex
        parsed_url = urlparse(link)
        pdf_filename = os.path.basename(parsed_url.path)

        filename = os.path.join("election_pdfs", pdf_filename)

        # Ensure unique filenames
        counter = 1
        while os.path.exists(filename):
            name, ext = os.path.splitext(pdf_filename)
            filename = os.path.join("election_pdfs", f"{name}_{counter}{ext}")
            counter += 1
        
        # Download the PDF
        response = requests.get(link)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {link}")

scrape_pdfs("https://history.house.gov/Institution/Election-Statistics/Election-Statistics/")