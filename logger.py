import logging

# Create a custm logger, that logs into file
# and it's formatted with date
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler = logging.FileHandler("app.logs")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
