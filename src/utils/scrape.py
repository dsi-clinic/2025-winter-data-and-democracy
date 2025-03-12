"""
Web scraping utilities for the project.

This module contains functions to scrape data from websites, download resources
such as PDFs, and save them locally.
"""
import random
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from config import PDF_DIR, SCRAPE_URL

# HTTP status code constants
HTTP_OK = 200


def is_valid_pdf_url(url):
    """Check if a URL likely points to a PDF based on extension or path components.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL likely points to a PDF, False otherwise.
    """
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    # Check file extension
    if path.endswith('.pdf'):
        return True
    
    # Check if 'pdf' appears in the path segments
    path_parts = path.split('/')
    return any('pdf' in part.lower() for part in path_parts)


def extract_year_from_url(url):
    """Extract a year (between 1900-2100) from a URL if present.

    Args:
        url (str): The URL to extract a year from.

    Returns:
        str or None: The extracted year as a string, or None if no year was found.
    """
    # Try to find a 4-digit year in the URL
    match = re.search(r'(?:^|[^\d])((?:19|20)\d{2})(?:[^\d]|$)', url)
    if match:
        return match.group(1)
    return None


def scrape_pdfs(url: str) -> None:
    """Scrape PDF links from a given website and download them to a local directory.
    
    Args:
        url (str): The URL of the website to scrape PDFs from.
        
    Raises:
        ValueError: If the URL provided is not a valid string.
    """
    if not isinstance(url, str) or not url.startswith("http"):
        raise ValueError("Invalid URL provided. Please enter a valid URL.")
    
    print(f"Starting scraper with URL: {url}")
    
    # Ensure the download directory exists
    PDF_DIR.mkdir(exist_ok=True, parents=True)
    print(f"Download directory: {PDF_DIR}")
    
    # Set to store unique URLs to visit
    to_visit = {url}
    # Set to store URLs already visited
    visited = set()
    # Set to store potential PDF URLs
    pdf_links = set()
    # Dictionary to store year-URL mappings
    year_pages = {}
    
    # Headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Get the base domain to stay within the same site
    parsed_base = urlparse(url)
    base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
    
    try:
        # Limit the number of pages to crawl to avoid excessive requests
        max_pages = 100
        page_count = 0
        
        while to_visit and page_count < max_pages:
            # Get the next URL to visit
            current_url = to_visit.pop()
            visited.add(current_url)
            page_count += 1
            
            print(f"\nVisiting page {page_count}/{max_pages}: {current_url}")
            
            try:
                # Add a small delay to avoid overwhelming the server
                # Using time.sleep with a fixed value to avoid S311 warning
                time.sleep(0.75)
                
                # Send a GET request to the URL
                response = requests.get(current_url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # Check if this is a PDF
                content_type = response.headers.get('Content-Type', '').lower()
                if 'application/pdf' in content_type:
                    pdf_links.add(current_url)
                    print(f"Found PDF directly: {current_url}")
                    continue
                
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract year from the current URL
                current_year = extract_year_from_url(current_url)
                if current_year:
                    year_pages[current_year] = current_url
                    print(f"Associated year {current_year} with URL: {current_url}")
                
                # Find all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href)
                    
                    # Skip external domains and non-HTTP(S) URLs
                    if not full_url.startswith(base_domain) or not full_url.startswith(('http://', 'https://')):
                        continue
                    
                    # Check if this is a PDF link
                    if is_valid_pdf_url(full_url):
                        pdf_links.add(full_url)
                        print(f"Found PDF link: {full_url}")
                        continue
                    
                    # Check if this is an election-related page
                    if ('election' in full_url.lower() or 
                        'statistic' in full_url.lower() or 
                        'data' in full_url.lower() or
                        'report' in full_url.lower() or
                        'document' in full_url.lower()):
                        
                        year = extract_year_from_url(full_url)
                        if year:
                            year_pages[year] = full_url
                            print(f"Found year-specific page: {year} - {full_url}")
                        
                        # Add to visit queue if not already visited
                        if full_url not in visited and full_url not in to_visit:
                            to_visit.add(full_url)
                            print(f"Added to queue: {full_url}")
                    
                    # Look for download buttons or links
                    link_text = link.get_text().lower()
                    if ('download' in link_text or
                        'pdf' in link_text or
                        'report' in link_text or
                        'statistic' in link_text):
                        
                        # This might be a download link
                        if full_url not in visited and full_url not in to_visit:
                            to_visit.add(full_url)
                            print(f"Added potential download link to queue: {full_url}")
                
                # Also check for forms with 'download' or related text
                for form in soup.find_all('form'):
                    form_text = form.get_text().lower()
                    if ('download' in form_text or 
                        'pdf' in form_text or
                        'report' in form_text):
                        
                        # Extract the form's action URL
                        action = form.get('action')
                        if action:
                            form_url = urljoin(current_url, action)
                            if form_url not in visited and form_url not in to_visit:
                                to_visit.add(form_url)
                                print(f"Added form action to queue: {form_url}")
                
            except Exception as e:
                print(f"Error visiting {current_url}: {str(e)}")
        
        # Convert the set to a list for processing
        pdf_links = list(pdf_links)
        print(f"\nFound {len(pdf_links)} potential PDF links")
        
        # If no PDFs found, try one more approach: look for PDF links in election year pages
        if not pdf_links and year_pages:
            print("\nNo PDFs found directly. Trying focused year-page search...")
            
            for year, page_url in year_pages.items():
                print(f"Deeply scanning year page for {year}: {page_url}")
                
                # Skip if already visited
                if page_url in visited:
                    continue
                
                try:
                    # Using fixed sleep time to avoid S311 warning
                    time.sleep(0.75)
                    response = requests.get(page_url, headers=headers, timeout=30)
                    
                    if response.status_code == HTTP_OK:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look specifically for PDF links
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            full_url = urljoin(page_url, href)
                            
                            # Check if this is a PDF link
                            if is_valid_pdf_url(full_url) and full_url not in pdf_links:
                                pdf_links.append(full_url)
                                print(f"Found PDF link on year page: {full_url}")
                                
                        # Look for iframe sources that might be PDFs
                        for iframe in soup.find_all('iframe', src=True):
                            src = iframe['src']
                            full_url = urljoin(page_url, src)
                            
                            if is_valid_pdf_url(full_url) and full_url not in pdf_links:
                                pdf_links.append(full_url)
                                print(f"Found PDF in iframe: {full_url}")
                except Exception as e:
                    print(f"Error scanning year page {page_url}: {str(e)}")
        
        # Download the PDFs
        successful_downloads = 0
        
        for link in pdf_links:
            # Try to extract year from the URL for naming
            year = extract_year_from_url(link)
            
            # Generate filename either from year or URL path
            if year:
                pdf_filename = f"{year}.pdf"
            else:
                # Extract filename from URL
                parsed_url = urlparse(link)
                path = parsed_url.path
                pdf_filename = path.split('/')[-1] if path else "unnamed_file.pdf"
                if not pdf_filename.endswith('.pdf'):
                    pdf_filename += '.pdf'
            
            # Ensure unique filenames
            filename = PDF_DIR / pdf_filename
            counter = 1
            while filename.exists():
                name, ext = filename.stem, filename.suffix
                filename = PDF_DIR / f"{name}_{counter}{ext}"
                counter += 1
            
            # Download the PDF
            try:
                print(f"Downloading: {link}")
                pdf_response = requests.get(link, headers=headers, timeout=60)
                
                # Check if it's a valid PDF by looking at content type and size
                content_type = pdf_response.headers.get('Content-Type', '').lower()
                is_pdf = ('application/pdf' in content_type or
                          link.lower().endswith('.pdf'))
                
                min_pdf_size = 1000  # Minimum size for a valid PDF (1KB)
                if pdf_response.status_code == HTTP_OK and is_pdf and len(pdf_response.content) > min_pdf_size:
                    with filename.open("wb") as file:
                        file.write(pdf_response.content)
                    successful_downloads += 1
                    print(f"Successfully downloaded: {filename} ({len(pdf_response.content)} bytes)")
                else:
                    if pdf_response.status_code != HTTP_OK:
                        print(f"Failed to download: {link}, Status code: {pdf_response.status_code}")
                    elif len(pdf_response.content) <= min_pdf_size:
                        print(f"Skipping: {link}, Too small to be valid PDF ({len(pdf_response.content)} bytes)")
                    else:
                        print(f"Skipping: {link}, Not a valid PDF")
            except Exception as e:
                print(f"Error downloading {link}: {str(e)}")
        
        print(f"\nSuccessfully downloaded {successful_downloads} out of {len(pdf_links)} potential PDFs")
    
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Scrape PDFs using the default URL from config
    scrape_pdfs(SCRAPE_URL)
    print("Scraping completed")
