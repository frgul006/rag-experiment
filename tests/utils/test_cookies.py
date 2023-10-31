import os
import tempfile
import unittest

from regent_rag.core.cookies import get_cookies_and_user_agent_from_file


class TestGetCookiesAndUserAgent(unittest.TestCase):
    def test_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            get_cookies_and_user_agent_from_file("non_existent_file.txt")

    def test_no_cookie_line(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write("-H 'user-agent: TestAgent'".encode())
            temp_path = temp.name

        with self.assertRaises(ValueError) as context:
            get_cookies_and_user_agent_from_file(temp_path)

        self.assertTrue("No cookie line found" in str(context.exception))
        os.remove(temp_path)

    def test_no_user_agent(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write("-H 'cookie: name=value'".encode())
            temp_path = temp.name

        with self.assertRaises(ValueError) as context:
            get_cookies_and_user_agent_from_file(temp_path)

        self.assertTrue("No user agent found" in str(context.exception))
        os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
