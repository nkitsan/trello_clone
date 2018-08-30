import datetime


HOST = 'http://127.0.0.1:8000/'
api = 'qmMry28x9fYFcarKCKEhR4taUYVnIm6Z'
TIME_PATTERN = '%Y-%m-%d %H:%M'


def date_validation(date):
    try:
        datetime.datetime.strptime(date, TIME_PATTERN)
    except ValueError:
        return False
    return True
