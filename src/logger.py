import logging

level = logging.INFO

logging.basicConfig(
    level=level,
    format="%(asctime)s %(name)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("test")
logger.setLevel(level)

# logger.error("test log")