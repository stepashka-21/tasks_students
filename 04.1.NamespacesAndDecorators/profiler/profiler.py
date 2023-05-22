import datetime
from functools import wraps


def profiler(func):  # type: ignore
    """
    Returns profiling decorator, which counts calls of function
    and measure last function execution time.
    Results are stored as function attributes: `calls`, `last_time_taken`
    :param func: function to decorate
    :return: decorator, which wraps any function passed
    """
    calls = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal calls
        if not calls:
            wrapper.calls = 0
        wrapper.calls += 1
        calls += 1
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        calls -= 1
        end_time = datetime.datetime.now()
        time_taken = (end_time - start_time).total_seconds()
        wrapper.last_time_taken = time_taken
        return result

    wrapper.calls = 0
    wrapper.last_time_taken = 0
    return wrapper
