from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from regent_rag.core.logging import logger
from regent_rag.core.security import mask_string


class Settings(BaseSettings):
    """
    This class extends the BaseSettings class from pydantic_settings.
    It defines the configuration settings for the application.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", frozen=True, extra="ignore")

    curl_file: str = "./request.curl"  # CURL_FILE
    embeddings_model: str = "text-embedding-ada-002"  # EMBEDDINGS_MODEL
    log_level: str = "INFO"  # LOG_LEVEL
    openai_api_key: str = ""  # OPENAI_API_KEY
    openai_model: str = "gpt-3.5-turbo"  # OPENAI_MODEL
    openai_temperature: float = 0.2  # OPENAI_TEMPERATURE
    output_folder: str = "./out"  # OUTPUT_FOLDER
    pinecone_api_key: str = ""  # PINECONE_API_KEY
    pinecone_environment: str = ""  # PINECONE_ENVIRONMENT
    pinecone_index_name: str = ""  # PINECONE_INDEX_NAME
    pinecone_text_field: str = "text"  # PINECONE_TEXT_FIELD
    flask_app: str = "./regent_rag/app.py"  # FLASK_APP


@lru_cache
def get_settings() -> Settings:
    """
    This function returns an instance of the Settings class.
    It uses the lru_cache decorator to cache the results of its most recent calls.
    If it's called again with the same arguments, it will return the stored result instead of recomputing the result.
    """
    settings = Settings()
    logger.debug("#### SETTINGS ####")
    logger.debug(f"curl_file: {settings.curl_file}")
    logger.debug(f"embeddings_model: {settings.embeddings_model}")
    logger.debug(f"log_level: {settings.log_level}")
    logger.debug(f"openai_api_key: {mask_string(settings.openai_api_key)}")
    logger.debug(f"openai_model: {settings.openai_model}")
    logger.debug(f"openai_temperature: {settings.openai_temperature}")
    logger.debug(f"output_folder: {settings.output_folder}")
    logger.debug(f"pinecone_api_key: {mask_string(settings.pinecone_api_key)}")
    logger.debug(f"pinecone_environment: {settings.pinecone_environment}")
    logger.debug(f"pinecone_index_name: {settings.pinecone_index_name}")
    logger.debug(f"flask_app: {settings.flask_app}")
    logger.debug("#### END OF SETTINGS ####")
    return settings
