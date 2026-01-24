import logging
from backend.core.config import settings

FORMAT = "%(asctime)s: [%(levelname)s](%(name)s) --> %(message)s"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=FORMAT,
        handlers=[logging.FileHandler(f"backend/logs/{settings.LOGS_FILE}")]
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)