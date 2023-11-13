import re
from typing import Dict, Tuple

from regent_rag.core.logging import logger


def get_cookies_and_user_agent_from_file(filepath: str) -> Tuple[Dict[str, str], str]:
    """
    Extracts cookies and user-agent from a file.

    Parameters:
    filepath (str): The path of the file.

    Returns:
    Tuple[Dict[str, str], str]: A tuple containing a dictionary of cookies and a string of user-agent.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # Extract cookie line
    cookie_line_match = re.search(r"-H ['|\"]cookie: (.*?)['|\"]", content, re.IGNORECASE)
    if cookie_line_match is None:
        raise ValueError(f"No cookie line found in file {filepath}")
    cookie_line = cookie_line_match.group(1)

    # Extract cookies
    cookies = {
        match.group(1).strip(): match.group(2).strip() for match in re.finditer(r"([^=]+)=([^;]+);?", cookie_line)
    }

    # Extract user agent
    user_agent_match = re.search(r"-H ['|\"]user-agent: (.*?)['|\"]", content, re.IGNORECASE)
    if user_agent_match is None:
        raise ValueError(f"No user agent found in file {filepath}")
    user_agent = user_agent_match.group(1)

    logger.info(f"Extracted cookies: {cookies}")
    logger.info(f"Extracted user-agent: {user_agent}")

    return cookies, user_agent
