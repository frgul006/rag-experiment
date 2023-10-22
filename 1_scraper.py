import json
import os
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from utils.cookies import get_cookies_and_user_agent_from_file
from utils.extractors import extract_text_from_pdf, extract_text_from_pptx
from utils.logging import logger
from utils.path import ensure_dir

CURL_FILE = "0_request.curl"
OUTPUT_FOLDER = "./out/scrape"


def scrape_website(
    session: requests.Session,
    url: str,
    visited: Optional[set[str]] = None,
    domain: Optional[str] = None,
    executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=10),
) -> None:
    visited = visited or set()
    domain = domain or urlparse(url).netloc

    logger.info(f"Downloading {url}...")

    # Parse the URL to create a filename
    filename = os.path.join(OUTPUT_FOLDER, f"{urllib.parse.quote_plus(url)}.json")

    # Download the HTML content of the webpage
    response = session.get(url)
    is_file = False

    if url.endswith(".pdf"):
        text_content = extract_text_from_pdf(response.content)
        is_file = True
    elif url.endswith(".pptx"):
        text_content = extract_text_from_pptx(response.content)
        is_file = True
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        text_content = str(soup)

    # Save the URL and the downloaded content into a JSON object
    data = {"url": url, "content": text_content}

    # Write the JSON object to a file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)

    # Add the URL to the set of visited pages
    visited.add(url)

    # If the URL was a file, return early, do not scan for links
    if is_file:
        return

    # Find all links on the webpage
    links = list({a["href"] for a in soup.find_all("a") if a.has_attr("href")})

    for href in links:
        # Make sure the URL is not None
        if href is not None:
            linkDomain = urlparse(href).netloc
            # Make sure the URL is not already visited and in the right domain
            if href not in visited and linkDomain == domain:
                # Handle relative URLs
                href = urllib.parse.urljoin(url, href)
                # Recursively scrape the linked webpage
                executor.submit(
                    scrape_website, session, href, visited, domain, executor
                )


def main() -> None:
    if not os.path.isfile(CURL_FILE):
        logger.critical(f"Error: File {CURL_FILE} does not exist!")
        sys.exit(1)

    # Get cookie and user_agent from request.curl file
    cookies, user_agent = get_cookies_and_user_agent_from_file(CURL_FILE)

    # Ensure output folders exist
    ensure_dir(OUTPUT_FOLDER)

    # Start scraping
    with requests.Session() as session:
        session.cookies.update(cookies)
        session.headers.update({"User-Agent": user_agent})
        scrape_website(session, "https://intern.regent.se/en/intranat-english")


if __name__ == "__main__":
    main()
