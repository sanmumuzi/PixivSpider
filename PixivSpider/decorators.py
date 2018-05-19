import time
from functools import wraps
import logging


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        mode = 'Spend time ({}.{}) : {}s.'
        logging.debug(mode.format(func.__module__, func.__name__, end - start))
        return result
    return wrapper


def return_auth_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return_dict = {}
        result = func(*args, **kwargs)
        return_dict['base_info'] = result
