# core/logger.py

import logging
from pathlib import Path

LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def setup_logger(name="sonderbot", level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(LOG_DIR / f"{name}.log")
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger
