import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

_ROOT_DIRECTORY: Path = Path(__file__).resolve().parent.parent
LOG_FILE_PATH = Path.joinpath(_ROOT_DIRECTORY, "logs/app.log")

LOG_FORMAT = "%(asctime)s - [%(levelname)s] - [%(module)s - %(funcName)s - %(lineno)d] - %(message)s"

logger = logging.getLogger()

formatter = logging.Formatter(fmt=LOG_FORMAT)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(
    LOG_FILE_PATH,
    mode='a',
    encoding="utf-8",
    maxBytes=1 * 1024 * 1024,  # 1Mb
    backupCount=3,
)
file_handler.setFormatter(formatter)

logger.handlers = [
    stream_handler,
    file_handler
]

logger.setLevel(logging.INFO)
