import time
from functools import wraps


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        mode = 'Spend time ({}.{}) : {}s.'
        print(mode.format(func.__module__, func.__name__, end - start))
        return result
    return wrapper
