import logging, os
def setup_logging():
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=level, format="[%(levelname)s] %(asctime)s %(name)s: %(message)s")

