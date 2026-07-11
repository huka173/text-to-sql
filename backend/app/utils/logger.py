import logging
from pathlib import Path

LOG_DIR = Path("/app/logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger("text_to_sql")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler = logging.FileHandler(LOG_FILE)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)