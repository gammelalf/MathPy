import math as _math
from functools import wraps as _wraps
from typing import TypeVar as _TypeVar
from typing import Dict as _Dict


_Numeric = _TypeVar("_Numeric", int, float, complex)


class _OperatorMeta(type):

    REGISTRY = {}

    def __init__(cls, name, bases, dct):
        super(_OperatorMeta, cls).__init__(name, bases, dct)
        if dct["SYMBOL"] is not None:
            _OperatorMeta.REGISTRY[dct["SYMBOL"]] = cls


class Operator(metaclass=_OperatorMeta):

    SYMBOL = None

    @property
    def priority(self):
        raise NotImplementedError()

    def binary(self, x, y):
        raise NotImplementedError(f"{self} can't be used as a binary operator")

    def unary(self, x):
        raise NotImplementedError(f"{self} can't be used as a unary operator")

    def __call__(self, right, left=None):
        if left is None:
            return self.unary(right)
        else:
            return self.binary(left, right)

    @staticmethod
    def handle_callables(func):
        @_wraps(func)
        def new_func(self, x, y):
            if callable(x) and callable(y):
                return lambda i: func(self, x(i), y(i))
            elif callable(x):
                return lambda i: func(self, x(i), y)
            elif callable(y):
                return lambda i: func(self, x, y(i))
            else:
                return func(self, x, y)
        return new_func

    @staticmethod
    def get(symbol: str) -> "Operator":
        return _OperatorMeta.REGISTRY[symbol]()

    @staticmethod
    def is_operator(symbol: str) -> bool:
        return symbol in _OperatorMeta.REGISTRY

    def __repr__(self):
        return self.__class__.__name__+"()"

    def __str__(self):
        return self.__class__.SYMBOL


class _Node:

    MATH_CONST = {
        "e": _math.e,
        "pi": _math.pi,
        "i": 1j
    }

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        raise NotImplementedError()

    def eval(self, **namespace: _Numeric) -> _Numeric:
        namespace = dict(_Node.MATH_CONST, **namespace)
        return self._eval(namespace)

    def __call__(self):
        return self.eval()


class BinOp(_Node):

    def __init__(self, left: _Node, operator: Operator, right: _Node):
        self.left = left
        self.right = right
        self.operator = operator

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        return self.operator(self.right._eval(namespace), self.left._eval(namespace))


class UnaryOp(_Node):

    def __init__(self, operator: Operator, child: _Node):
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
