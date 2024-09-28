import logging
import logging.config
from datetime import datetime
from pathlib import Path

from src.settings import Settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "root": {"level": "INFO", "handlers": ["console", "file"]},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "console",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "file",
            "filename": "%(logfilename)s",
            "mode": "a",
            "encoding": "utf-8",
        },
    },
    "formatters": {
        "console": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%H:%M:%S",
        },
        "file": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s"
        },
    },
}


def set_up_loggers(settings: Settings) -> None:
    """Load logging configuration"""
    timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

    logfilename = (
        Path(settings.app.log_directory) / f"Credict_Score_Logs_{timestamp}.log"
    )

    LOGGING_CONFIG["handlers"]["file"]["filename"] = logfilename
    logging.config.dictConfig(LOGGING_CONFIG)
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.disabled = True
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").propagate = False
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
