from functools import wraps
import threading


def decorator_thread(func_name):  # thread decorator: create a Thread object for func_name
    def inner(func):
        @wraps(func)
        def wrapper(picture_id, status, usr, password):
            threading_item = threading.Thread(target=func_name, args=(picture_id, status, usr, password))
            threading_item.setDaemon(True)
            threading_item.start()
        return wrapper
    return inner