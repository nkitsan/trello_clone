import logging
from datetime import datetime
from functools import wraps

import os


from tasker.libs.logger.config import (LOGGER_NAME,
                                       LOG_LEVEL,
                                       LOG_DIRECTORY,
                                       LOG_FORMAT)


def get_logger(logger_name):
    return logging.getLogger(logger_name)


def configure_logging(logger_name=LOGGER_NAME,
                      level=LOG_LEVEL,
                      log_directory=LOG_DIRECTORY,
                      log_format=LOG_FORMAT,
                      log_filename=None):
    """
    Configure logging to log file
    """
    log_level_dict = {"CRITICAL": logging.CRITICAL,
                      "DEBUG": logging.DEBUG,
                      "ERROR": logging.ERROR}
    level = log_level_dict[level]
    if not log_filename:
        log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'

    logger = get_logger(logger_name)
    logger.setLevel(level)

    formatter = logging.Formatter(log_format)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)
    if not os.path.exists(log_directory + log_filename):
        open(log_directory + "/" + log_filename, "w+")

    handler = logging.FileHandler(filename=log_directory + "/" + log_filename)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_logs(func):
    """
    This decorator provides logging activities for calling functions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        configure_logging()
        logger = get_logger(LOGGER_NAME)
        try:
            print("Called : {}".format(func.__name__))
            print("Args: {}".format(args))
            logger.debug("Called : {}".format(func.__name__))
            logger.debug("Args: {}".format(args))
            result = func(*args, **kwargs)
            return result
        except Exception as ex:
            logger.error(ex)
            raise
    return wrapper
