import json
import os
import tempfile
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock, patch

import pytest

from regent_rag import scrape

URL_ROOT = "https://intern.regent.se/en/intranat-english"
URL_LINK_HREF = "https://intern.regent.se/en/link1"


class TestScrapeWebsite:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.url = URL_ROOT
        self.cookies = {"cookie1": "value1"}
        self.user_agent = "test_agent"
        self.visited: set[str] = set()
        self.domain = "intern.regent.se"

        # Create temporary directory for output
        self.output_dir = tempfile.TemporaryDirectory()
        self.orig_scrape_folder = scrape.SCRAPE_FOLDER
        scrape.SCRAPE_FOLDER = self.output_dir.name  # type: ignore

        yield  # this is where the testing happens

        # Reset SCRAPE_FOLDER to its original value
        scrape.SCRAPE_FOLDER = self.orig_scrape_folder  # type: ignore

        # Clean up the temporary directory
        self.output_dir.cleanup()

    @patch.object(scrape, "logger")
    @patch.object(scrape, "requests")
    @patch.object(scrape, "BeautifulSoup")
    def test_scrape_website(
        self,
        mock_soup: MagicMock,
        mock_get: MagicMock,
        _: MagicMock,
    ):
        # Set up the mocked responses
        mock_response = MagicMock()

        mock_response.text = f"<html><body><a href='{URL_LINK_HREF}'>Link1</a></body></html>"
        mock_get.get.return_value = mock_response

        mock_link = MagicMock()
        mock_link.has_attr.return_value = True
        mock_link.__getitem__.return_value = URL_LINK_HREF

        mock_soup.return_value.find_all.return_value = [mock_link]

        # Run the function
        with ThreadPoolExecutor(max_workers=1) as executor:
            scrape.scrape_website(mock_get, self.url, executor=executor)

        # Check that the requests.get function was called with the correct arguments
        expected_calls = [
            ((self.url,),),
            ((URL_LINK_HREF,),),
        ]
        assert all(call in mock_get.get.call_args_list for call in expected_calls)

        # Check that the BeautifulSoup function was called with the correct arguments
        mock_soup.assert_called_with(mock_response.text, "html.parser")

        # Check that the output files were created and contain the correct data
        for url in [self.url, URL_LINK_HREF]:
            filename = os.path.join(self.output_dir.name, f"{urllib.parse.quote_plus(url)}.json")
            assert os.path.isfile(filename)

            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert data == {"url": url, "content": str(mock_soup.return_value)}
