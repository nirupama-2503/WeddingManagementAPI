import logging
from pathlib import Path


def setup_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format
    )

    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "app.log"

    root_logger = logging.getLogger()

    # Avoid adding duplicate file handlers
    if not any(
        isinstance(handler, logging.FileHandler)
        and Path(handler.baseFilename) == log_file.resolve()
        for handler in root_logger.handlers
    ):
        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(log_format))

        root_logger.addHandler(file_handler)