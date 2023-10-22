import os

from dotenv import load_dotenv

from utils.logging import logger
from utils.security import mask_string


def load_config() -> tuple[str, str, str, str]:
    load_dotenv()

    default_values = {
        "OPENAI_API_KEY": None,
        "PINECONE_API_KEY": None,
        "PINECONE_INDEX_NAME": None,
        "PINECONE_ENVIRONMENT": None,
    }

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default_values["OPENAI_API_KEY"])
    PINECONE_API_KEY = os.environ.get(
        "PINECONE_API_KEY", default_values["PINECONE_API_KEY"]
    )
    PINECONE_INDEX_NAME = os.environ.get(
        "PINECONE_INDEX_NAME", default_values["PINECONE_INDEX_NAME"]
    )
    PINECONE_ENVIRONMENT = os.environ.get(
        "PINECONE_ENVIRONMENT", default_values["PINECONE_ENVIRONMENT"]
    )

    assert OPENAI_API_KEY, "OPENAI_API_KEY is not set"
    assert PINECONE_API_KEY, "PINECONE_API_KEY is not set"
    assert PINECONE_INDEX_NAME, "PINECONE_INDEX_NAME is not set"
    assert PINECONE_ENVIRONMENT, "PINECONE_ENVIRONMENT is not set"

    logger.debug(f"OPENAI_API_KEY: {mask_string(OPENAI_API_KEY)}")
    logger.debug(f"PINECONE_API_KEY: {mask_string(PINECONE_API_KEY)}")
    logger.debug(f"PINECONE_INDEX_NAME: {PINECONE_INDEX_NAME}")
    logger.debug(f"PINECONE_ENVIRONMENT: {PINECONE_ENVIRONMENT}")

    return OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_ENVIRONMENT
