import time
import logging
from typing import Callable, ParamSpec, TypeVar
import functools

_P = ParamSpec("_P")
_R = TypeVar("_R")


class BenchmarkHarness:

    def __init__(self) -> None:
        pass
    def benchmark(
        self,
        outer_func: Callable[_P, _R] | None = None,
        *,
        warmup_rounds: int = 0,
        delay: int = 0,
    ):
        def dec(func: Callable[_P, _R]) -> Callable[_P, _R]:
            @functools.wraps(func)
            def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _R:
                for _ in range(warmup_rounds):
                    func(*args, **kwargs)
                start = time.perf_counter()
                time.sleep(delay)
                result = func(*args, **kwargs)
                end = time.perf_counter()
                print(f"{func.__name__} took {end - start:2f} seconds")
                return result
            return wrapped
        return dec(outer_func) if outer_func else dec


harness = BenchmarkHarness()


@harness.benchmark
def add(x, y):
    print("adding")
    return x + y


def main():
    add(1, 2)


if __name__ == "__main__":
    main()
