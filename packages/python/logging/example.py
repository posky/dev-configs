import logging.config

# pip install pyyaml
import yaml

# Load the config file
with open("logging.yaml") as f:
    config = yaml.safe_load(f.read())

# Configure the logging module with the config file
logging.config.dictConfig(config)

# Get a logger object
logger = logging.getLogger("development")

# Log some message
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")


# Get a logger object
logger = logging.getLogger("staging")

# Log some message
logger.debug("This is a debug message - staging")
logger.info("This is an info message - staging")
logger.warning("This is a warning message - staging")
logger.error("This is an error message - staging")
logger.critical("This is a critical message - staging")
