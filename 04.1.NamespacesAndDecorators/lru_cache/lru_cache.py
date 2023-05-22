from functools import wraps
from typing import Callable, Any, TypeVar
from collections import OrderedDict

Function = TypeVar('Function', bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """

    def decorator(func: Function) -> Function:
        dict_res: OrderedDict = OrderedDict()

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = args, tuple(sorted(kwargs.items()))

            if key in dict_res:
                dict_res.move_to_end(key)

            else:
                dict_res[key] = func(*args, **kwargs)

                if len(dict_res) > max_size:
                    dict_res.popitem(last=False)

            return dict_res[key]
        return wrapper
    return decorator