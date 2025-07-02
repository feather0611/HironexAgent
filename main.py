import sys
import logging

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG) # 設定根記錄器的級別

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    stream_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S %p'
    )

    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

if __name__ == "__main__":
    
    setup_logging()
    logger = logging.getLogger(__name__)