from typing import Callable as _Callable
from functools import wraps as _wraps


class Operator:

    def __init__(self, symbol: str, priority: int, unary: _Callable = None, binary: _Callable = None):
        self.symbol = symbol
        self.priority = priority
        self.unary = unary
        self.binary = binary

    def __call__(self, x, y=None):
        if y is None:
            return self.unary(x)
        else:
            return self.binary(x, y)

    @staticmethod
    def handle_callables(func):
        @_wraps(func)
        def new_func(x, y):
            if callable(x) and callable(y):
                return lambda i: func(x(i), y(i))
            elif callable(x):
                return lambda i: func(x(i), y)
            elif callable(y):
                return lambda i: func(x, y(i))
            else:
                return func(x, y)
        return new_func

    def __repr__(self):
        return f"Operator({self.symbol})"

    def __str__(self):
        return self.symbol
