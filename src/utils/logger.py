import logging
import logging.config
import os

def setup_logging(default_level=logging.INFO, config_file='config/logging.conf'):
    """
    Set up logging configuration.
    
    Args:
        default_level (int): Default log level if the config file is missing.
        config_file (str): Path to the logging configuration file.
    """
    if os.path.exists(config_file):
        logging.config.fileConfig(config_file, disable_existing_loggers=False)
    else:
        # Fallback to basic logging if the config file is missing
        logging.basicConfig(level=default_level)
        logger = logging.getLogger(__name__)
        logger.warning(f"Logging configuration file '{config_file}' not found. Using default configuration.")

def get_logger(logger_name):
    """
    Get a logger instance with the given name.
    
    Args:
        logger_name (str): The name of the logger to retrieve.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(logger_name)

# Example of logging setup
if __name__ == "__main__":
    setup_logging()
    logger = get_logger('fix_logger')
    logger.info("Logger has been set up.")
