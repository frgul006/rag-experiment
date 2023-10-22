import importlib
import json
import os
import tempfile
import unittest
import urllib.parse
from typing import Any
from unittest.mock import MagicMock, patch

scraper = importlib.import_module("1_scraper")

URL_ROOT = "https://intern.regent.se/en/intranat-english"
URL_LINK_HREF = "https://intern.regent.se/en/link1"


class TestScrapeWebsite(unittest.TestCase):
    def setUp(self) -> None:
        self.url = URL_ROOT
        self.cookies = {"cookie1": "value1"}
        self.user_agent = "test_agent"
        self.visited: set[str] = set()
        self.domain = "intern.regent.se"

        # Create temporary directory for output
        self.output_dir = tempfile.TemporaryDirectory()
        self.orig_output_folder = scraper.OUTPUT_FOLDER
        scraper.OUTPUT_FOLDER = self.output_dir.name  # type: ignore

    def tearDown(self) -> None:
        # Reset OUTPUT_FOLDER to its original value
        scraper.OUTPUT_FOLDER = self.orig_output_folder  # type: ignore

        # Clean up the temporary directory
        self.output_dir.cleanup()

    @patch.object(scraper, "print")
    @patch.object(scraper, "requests")
    @patch.object(scraper, "BeautifulSoup")
    def test_scrape_website(
        self,
        mock_soup: MagicMock,
        mock_get: MagicMock,
        _: MagicMock,
    ) -> None:
        # Set up the mocked responses
        mock_response = MagicMock()

        mock_response.text = (
            f"<html><body><a href='{URL_LINK_HREF}'>Link1</a></body></html>"
        )
        mock_get.get.return_value = mock_response

        mock_link = MagicMock()
        mock_link.has_attr.return_value = True
        mock_link.__getitem__.return_value = URL_LINK_HREF

        mock_soup.return_value.find_all.return_value = [mock_link]

        # Run the function
        scraper.scrape_website(mock_get, self.url)

        # Check that the requests.get function was called with the correct arguments
        expected_calls = [
            ((self.url,),),
            ((URL_LINK_HREF,),),
        ]
        self.assertEqual(mock_get.get.call_args_list, expected_calls)

        # Check that the BeautifulSoup function was called with the correct arguments
        mock_soup.assert_called_with(mock_response.text, "html.parser")

        # Check that the output files were created and contain the correct data
        for url in [self.url, URL_LINK_HREF]:
            filename = os.path.join(
                self.output_dir.name, f"{urllib.parse.quote_plus(url)}.json"
            )
            self.assertTrue(os.path.isfile(filename))

            with open(filename, "r") as f:
                data = json.load(f)
                self.assertEqual(
                    data, {"url": url, "content": str(mock_soup.return_value)}
                )


if __name__ == "__main__":
    unittest.main()
