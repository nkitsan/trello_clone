import datetime
import os
from pathlib import Path


HOST = 'http://127.0.0.1:8000/'
TIME_PATTERN = '%Y-%m-%d %H:%M'
TASKER_PATH = os.path.join(str(Path.home()))


def date_validation(date):
    try:
        datetime.datetime.strptime(date, TIME_PATTERN)
    except ValueError:
        return False
    return True
