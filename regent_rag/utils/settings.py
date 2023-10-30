from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from regent_rag.utils.logging import logger
from regent_rag.utils.security import mask_string


class Settings(BaseSettings):
    """
    This class extends the BaseSettings class from pydantic_settings.
    It defines the configuration settings for the application.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", frozen=True)

    openai_api_key: str = ""  # OPENAI_API_KEY
    pinecone_api_key: str = ""  # PINECONE_API_KEY
    pinecone_index_name: str = ""  # PINECONE_INDEX_NAME
    pinecone_environment: str = ""  # PINECONE_ENVIRONMENT
    log_level: str = "INFO"  # LOG_LEVEL
    curl_file: str = "./request.curl"
    output_folder: str = "./out"


@lru_cache
def get_settings() -> Settings:
    """
    This function returns an instance of the Settings class.
    It uses the lru_cache decorator to cache the results of its most recent calls.
    If it's called again with the same arguments, it will return the stored result instead of recomputing the result.
    """
    settings = Settings()
    logger.debug("#### SETTINGS ####")
    logger.debug(f"openai_api_key: {mask_string(settings.openai_api_key)}")
    logger.debug(f"pinecone_api_key: {mask_string(settings.pinecone_api_key)}")
    logger.debug(f"pinecone_index_name: {settings.pinecone_index_name}")
    logger.debug(f"pinecone_environment: {settings.pinecone_environment}")
    logger.debug(f"log_level: {settings.log_level}")
    logger.debug(f"curl_file: {settings.curl_file}")
    logger.debug(f"output_folder: {settings.output_folder}")
    logger.debug("#### END OF SETTINGS ####")
    return settings
