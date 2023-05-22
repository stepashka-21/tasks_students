import time
import contextlib

import typing as tp


class TimeoutException(Exception):
    pass


class SoftTimeoutException(TimeoutException):
    pass


class HardTimeoutException(TimeoutException):
    pass


def soft(time: tp.Union[float, None]) -> str:
    return f"Soft timeout exceeded: {time:.4f} seconds"


def hard(time: tp.Union[float, None]) -> str:
    return f"Hard timeout exceeded: {time:.4f} seconds"


@contextlib.contextmanager
def TimeCatcher(soft_timeout: tp.Union[float, None] = None, hard_timeout: tp.Union[float, None] = None):
    assert soft_timeout is None or soft_timeout > 0, "Invalid soft_limit value"
    assert hard_timeout is None or hard_timeout > 0, "Invalid hard_limit value"
    if soft_timeout is not None and hard_timeout is not None:
        assert soft_timeout <= hard_timeout
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if soft_timeout is not None and elapsed_time > soft_timeout:
            raise SoftTimeoutException(soft(elapsed_time))
        if hard_timeout is not None and elapsed_time > hard_timeout:
            raise HardTimeoutException(hard(elapsed_time))

    class TimeCatcherResult:
        def __init__(self, soft_timeout: tp.Union[float, None] = None, hard_timeout: tp.Union[float, None] = None):
            assert soft_timeout is None or soft_timeout > 0, "Invalid soft_limit value"
            assert hard_timeout is None or hard_timeout > 0, "Invalid hard_limit value"
            if soft_timeout is not None and hard_timeout is not None:
                assert soft_timeout <= hard_timeout
            self.soft_timeout = soft_timeout
            self.hard_timeout = hard_timeout
            self.start_time = None
            self.end_time = None

        def __str__(self):
            elapsed = self.end_time - self.start_time if self.end_time else 0
            return f"Time consumed: {float(elapsed):.10f}"

        def __float__(self):
            return self.end_time - self.start_time if self.end_time else time.time() - self.start_time

    return TimeCatcherResult()
