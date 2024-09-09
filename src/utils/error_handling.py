import logging
import traceback

class FIXServiceError(Exception):
    """
    Base class for all custom exceptions in the FIX service.
    """
    pass


class ConfigurationError(FIXServiceError):
    """
    Raised when there is an issue with the configuration file or settings.
    """
    def __init__(self, message="Configuration error occurred"):
        super().__init__(message)


class ConnectionError(FIXServiceError):
    """
    Raised when there is a connection issue, such as failing to connect to the FIX server.
    """
    def __init__(self, message="Failed to connect to the FIX server"):
        super().__init__(message)


class MessageProcessingError(FIXServiceError):
    """
    Raised when there is an issue with processing FIX messages.
    """
    def __init__(self, message="Error processing FIX message"):
        super().__init__(message)


def log_and_raise(exception, logger=None):
    """
    Logs the error with a traceback and raises the exception.

    Args:
        exception (Exception): The exception to log and raise.
        logger (logging.Logger, optional): Logger to use. If None, defaults to root logger.
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    # Log the full traceback of the error
    logger.error(f"Exception occurred: {str(exception)}")
   
