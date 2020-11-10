"""
Implement a dice operator:

2d6 rolls two 6-sided dice and adds their results
"""

from random import randint as _randint

from expr_parser.operators.base import Operator as _Operator


Dice = _Operator(
    symbol="d",
    priority=100,
    unary=lambda x: _randint(1, x),
    binary=lambda x, y: sum((_randint(1, y) for i in range(x)))
)
