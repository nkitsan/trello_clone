import os


CORE_PATH = 'tasker'

LOGGER_NAME = "DAILY_TASKER_LOGGER"
LOG_FORMAT = ("(%(process)d/%(levelname)s:%(message)s:(%(asctime)s)")

LOG_FOLDER = "logs"
LOG_DIRECTORY = os.path.join(CORE_PATH, LOG_FOLDER)

LOG_LEVEL = "DEBUG"