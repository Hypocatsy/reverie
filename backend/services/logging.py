import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging() -> None:
    """Configure logging with console + daily rotating file output."""
    root = logging.getLogger("reverie")
    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (INFO+)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    root.addHandler(console)

    # Daily rotating file (DEBUG+) — one file per day, keep 30 days
    file_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, "reverie.log"),
        when="midnight",
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    root.addHandler(file_handler)

    # Separate error log
    error_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, "errors.log"),
        when="midnight",
        backupCount=30,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(fmt)
    root.addHandler(error_handler)
