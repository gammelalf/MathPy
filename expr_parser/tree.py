import math as _math
from typing import TypeVar as _TypeVar
from typing import Dict as _Dict

from expr_parser.operators.base import Operator as _Operator


_Numeric = _TypeVar("_Numeric", int, float, complex)


class _Node:

    MATH_CONST = {
        "e": _math.e,
        "pi": _math.pi,
        "i": 1j,
        "sin": _math.sin,
        "cos": _math.cos,
        "tan": _math.tan,
    }

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        raise NotImplementedError()

    def eval(self, **namespace: _Numeric) -> _Numeric:
        namespace = dict(_Node.MATH_CONST, **namespace)
        return self._eval(namespace)

    def __call__(self):
        return self.eval()


class BinOp(_Node):

    def __init__(self, left: _Node, operator: _Operator, right: _Node):
        self.left = left
        self.right = right
        self.operator = operator

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        return self.operator(self.right._eval(namespace), self.left._eval(namespace))


class UnaryOp(_Node):

    def __init__(self, operator: _Operator, child: _Node):
        self.child = child
        self.operator = operator

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        return self.operator(self.child._eval(namespace))


class Const(_Node):

    def __init__(self, value: _Numeric):
        self.value = value

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        return self.value

    def __repr__(self):
        return f"Const({repr(self.value)})"

    def __str__(self):
        return str(self.value)


class Var(_Node):

    def __init__(self, name: str):
        self.name = name

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        return namespace[self.name]

    def __repr__(self):
        return f"Var({repr(self.name)})"

    def __str__(self):
        return str(self.name)
