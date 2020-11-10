from typing import TypeVar as _TypeVar


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

    @staticmethod
    def get(symbol: str) -> "Operator":
        return _OperatorMeta.REGISTRY[symbol]()

    @staticmethod
    def is_operator(symbol: str) -> bool:
        return symbol in _OperatorMeta.REGISTRY

    def __call__(self, x, y):
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__+"()"

    def __str__(self):
        return self.__class__.SYMBOL


class _Add(Operator):

    SYMBOL = "+"

    @property
    def priority(self):
        return 0

    def __call__(self, x, y):
        return x + y


class _Sub(Operator):

    SYMBOL = "-"

    @property
    def priority(self):
        return 0

    def __call__(self, x, y):
        return x - y


class _Mul(Operator):

    SYMBOL = "*"

    @property
    def priority(self):
        return 10

    def __call__(self, x, y):
        return x * y


class _Div(Operator):

    SYMBOL = "/"

    @property
    def priority(self):
        return 10

    def __call__(self, x, y):
        return x / y


class _Pow(Operator):

    SYMBOL = "^"

    @property
    def priority(self):
        return 20

    def __call__(self, x, y):
        return x ** y


class _Node:

    def eval(self, **namespace: _Numeric) -> _Numeric:
        raise NotImplementedError()

    def __call__(self):
        return self.eval()


class Operation(_Node):

    def __init__(self, left: _Node, operator: Operator, right: _Node):
        self.left = left
        self.right = right
        self.operator = operator

    def eval(self, **namespace: _Numeric) -> _Numeric:
        return self.operator(self.left.eval(**namespace), self.right.eval(**namespace))


class Const(_Node):

    def __init__(self, value: _Numeric):
        self.value = value

    def eval(self, **namespace: _Numeric) -> _Numeric:
        return self.value

    def __repr__(self):
        return f"Const({repr(self.value)})"

    def __str__(self):
        return str(self.value)


class Var(_Node):

    def __init__(self, name: str):
        self.name = name

    def eval(self, **namespace: _Numeric) -> _Numeric:
        return namespace[self.name]

    def __repr__(self):
        return f"Var({repr(self.name)})"

    def __str__(self):
        return str(self.name)
