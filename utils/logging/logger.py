import logging
import os
from typing import Any, Dict, Optional

from colorama import Fore, Style
from dotenv import load_dotenv

LEVELS: Dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if record.levelno == logging.CRITICAL:
            prefix = f"{Fore.RED}{Style.BRIGHT}"
        elif record.levelno == logging.ERROR:
            prefix = f"{Fore.RED}"
        elif record.levelno == logging.WARNING:
            prefix = f"{Fore.YELLOW}"
        elif record.levelno == logging.INFO:
            prefix = f"{Fore.WHITE}"
        else:  # DEBUG and anything else
            prefix = f"{Fore.LIGHTBLACK_EX}"
        message = super().format(record)
        message = f"{prefix}{message}{Style.RESET_ALL}"
        return message


class SingletonLogger:
    _instance: Optional["SingletonLogger"] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "SingletonLogger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        load_dotenv()
        self._logger = logging.getLogger("SingletonLogger")
        self._logger.setLevel(
            LEVELS.get(os.environ.get("LOG_LEVEL", "INFO"), logging.INFO)
        )
        formatter = ColoredFormatter("%(asctime)s %(levelname)s %(message)s")

        # StreamHandler for console logging
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        # FileHandler for file logging if LOG_FILE is set
        log_file = os.environ.get("LOG_FILE")
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            self._logger.addHandler(fh)

        # Handler for uncaught exceptions
        logging.captureWarnings(True)

    def critical(self, *args: Any, **kwargs: Any) -> None:
        self._logger.critical(*args, **kwargs)

    def error(self, *args: Any, **kwargs: Any) -> None:
        self._logger.error(*args, **kwargs)

    def warning(self, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(*args, **kwargs)

    def info(self, *args: Any, **kwargs: Any) -> None:
        self._logger.info(*args, **kwargs)

    def debug(self, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(*args, **kwargs)
