import logging

# Create a logger
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
