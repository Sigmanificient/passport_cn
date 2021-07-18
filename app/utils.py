import time
from typing import Any, Callable

OriginalFunc = Callable[[Any], Any]
DecoratedFunc = Callable[[Any], Any]


def sleep_after(seconds: int) -> Callable[[OriginalFunc], DecoratedFunc]:
    def wrapper(func: OriginalFunc) -> DecoratedFunc:
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            r: Any = func(*args, **kwargs)
            time.sleep(seconds)
            return r

        return wrapped

    return wrapper
