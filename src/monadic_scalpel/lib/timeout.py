from functools import wraps
import errno
import os
import signal

from pymonad.Maybe import Nothing

def timeout(seconds=10, err_msg=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            return Nothing

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
