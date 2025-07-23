import os
import logging
import logging.handlers
from pathlib import Path

log_dir = Path("/app/logs")
log_dir.mkdir(exist_ok=True, mode=0o777)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            filename=log_dir / "app.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
    ]
)

logger = logging.getLogger("webapi-dicionario")
