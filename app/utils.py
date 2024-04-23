from functools import wraps
import logging

# Create a logger
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


def exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Log the error along with the function name
            logger.error(f"Error occurred in {func.__name__}: {str(e)}")
            raise e

    return wrapper
