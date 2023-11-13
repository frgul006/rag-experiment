import json
import os
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from regent_rag.core.cookies import get_cookies_and_user_agent_from_file
from regent_rag.core.extractors import extract_text_from_pdf, extract_text_from_pptx
from regent_rag.core.logging import logger
from regent_rag.core.path import ensure_dir
from regent_rag.core.settings import get_settings

CURL_FILE = get_settings().curl_file
SCRAPE_FOLDER = f"{get_settings().output_folder}/scrape"


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
    filename = os.path.join(SCRAPE_FOLDER, f"{urllib.parse.quote_plus(url)}.json")

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
        raw_soup = BeautifulSoup(response.text, "html.parser")
        soup = BeautifulSoup(response.text, "html.parser")
        # Remove script and style elements
        for script_or_style in soup(["script", "style", "link", "header", "footer"]):
            script_or_style.decompose()

        text_content = re.sub(r"[\n\t]", "", str(soup))

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
    links = list({a["href"] for a in raw_soup.find_all("a") if a.has_attr("href")})

    # If scraping root page and login link was found, log critical error and exit
    if url == "https://intern.regent.se/en/intranat-english" and any(
        "https://intern.regent.se/wp-login.php" in link for link in links
    ):
        logger.critical("Login link found on root page. You are not authenticated properly!")
        sys.exit(1)

    for href in links:
        # Make sure the URL is not None
        if href is not None:
            link_domain = urlparse(href).netloc
            # Make sure the URL is not already visited and in the right domain
            if href not in visited and link_domain == domain:
                # Handle relative URLs
                href = urllib.parse.urljoin(url, href)
                # Recursively scrape the linked webpage
                executor.submit(scrape_website, session, href, visited, domain, executor)


def main() -> None:
    if not os.path.isfile(CURL_FILE):
        logger.critical(f"Error: File {CURL_FILE} does not exist!")
        sys.exit(1)

    # Get cookie and user_agent from request.curl file
    cookies, user_agent = get_cookies_and_user_agent_from_file(CURL_FILE)

    # Ensure output folders exist
    ensure_dir(SCRAPE_FOLDER)

    # Start scraping
    with requests.Session() as session:
        session.cookies.update(cookies)
        session.headers.update({"User-Agent": user_agent})
        scrape_website(session, "https://intern.regent.se/en/intranat-english")


if __name__ == "__main__":
    main()
