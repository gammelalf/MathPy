import math

from base import Function
from complex import KoeffFunc as _KoeffFunc


class ConstFunc(Function):
    """
    f(x) = k
    """

    def __init__(self, value):
        self.c = value

    def _derive(self):
        return ConstFunc(0)

    def eval(self, x):
        return self.c

    def _format(self):
        return str(self.c)


class PowerFunc(Function):
    """
    f(x) = x^n
    """

    def __init__(self, power):
        self.n = power

    def _derive(self):
        return _KoeffFunc(self.n, PowerFunc(self.n-1))

    def eval(self, x):
        return x**self.n

    def _format(self):
        return f"{{x}}^{str(self.n)}"


class ExpFunc(Function):
    """
    e^x
    """

    def _derive(self):
        return self

    def eval(self, x):
        return math.exp(x)

    def _format(self):
        return "e^{x}"

