import pickle
from typing_extensions import Any, Callable, TypeVar, ParamSpec
import inspect
from pathlib import Path
from typing import Tuple

_R = TypeVar("_R")
_P = ParamSpec("_P")

def _build_key(
    func: Callable[_P, _R], *args, **kwargs
) -> Tuple[Tuple[str, Any], ...]:
    spec = inspect.getfullargspec(func)
    arg_pairs = list(zip(spec.args, args))
    for pair in kwargs.items():
        arg_pairs.append(pair)
    key = tuple(sorted(arg_pairs))
    return key


def persistent_cache(out_func: Callable[_P, _R] = None, output: Path | None = None):
    def dec(func):
        out_file = output if output else Path(f"{func.__name__}.pkl")
        cache = {}
        if out_file.exists():
            with out_file.open("rb") as f:
                cache = pickle.load(f)

        def wrapped(*args: _P.args, **kwargs: _P.kwargs):
            key = _build_key(func, *args, **kwargs)
            print(key)
            if key not in cache:
                result = func(*args, **kwargs)
                cache[key] = result
                with out_file.open("wb") as f:
                    pickle.dump(cache, f)
            return cache[key]

        return wrapped

    return dec(out_func) if out_func else dec


@persistent_cache
def add(x, y):
    return x + y


def main() -> None:
    add(3, 4)
    add(5, 4)


if __name__ == "__main__":
    main()
