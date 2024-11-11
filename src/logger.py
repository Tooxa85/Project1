import logging as log
from logging import Logger


def log_setup() -> Logger:
    """Логер"""
    logger = log.getLogger(__name__)
    logger.setLevel(log.DEBUG)
    file_handler = log.FileHandler("code.log", "w", encoding="utf-8")
    file_handler.setFormatter(log.Formatter("%(asctime)s - %(module)s, %(levelname)s: %(message)s"))
    logger.addHandler(file_handler)
    return logger
