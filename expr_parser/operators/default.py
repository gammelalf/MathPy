"""
Provide implementation for the basic math operators:

+, -, *, /, ^
"""

import operator as _op

from expr_parser.operators.base import Operator as _Operator


def _implicit(x, y):
    if callable(x) and callable(y):
        return lambda i: x(y(i))
    elif callable(x):
        return x(y)
    elif callable(y):
        return lambda i: x * y(i)
    else:
        return x * y


Implicit = _Operator(
    symbol="==IMPLICIT==",
    priority=10,
    binary=_implicit
)

Add = _Operator(
    symbol="+",
    priority=0,
    unary=lambda x: x,
    binary=_Operator.handle_callables(_op.add)
)

Sub = _Operator(
    symbol="-",
    priority=0,
    unary=_op.neg,
    binary=_Operator.handle_callables(_op.sub)
)

Mul = _Operator(
    symbol="*",
    priority=10,
    binary=_Operator.handle_callables(_op.mul)
)

Div = _Operator(
    symbol="/",
    priority=10,
    binary=_Operator.handle_callables(_op.truediv)
)

Pow = _Operator(
    symbol="^",
    priority=20,
    binary=_Operator.handle_callables(_op.pow)
)
