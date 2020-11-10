"""
Provide implementation for the basic math operators:

+, -, *, /, ^
"""

from expr_parser.tree import Operator as _Operator


class _Implicit(_Operator):

    SYMBOL = "==IMPLICIT=="

    @property
    def priority(self):
        return 10

    def binary(self, x, y):
        if callable(x) and callable(y):
            return lambda i: x(y(i))
        elif callable(x):
            return x(y)
        elif callable(y):
            return lambda i: x * y(i)
        else:
            return x * y


class _Add(_Operator):

    SYMBOL = "+"

    @property
    def priority(self):
        return 0

    @_Operator.handle_callables
    def binary(self, x, y):
        return x + y

    def unary(self, x):
        return x


class _Sub(_Operator):

    SYMBOL = "-"

    @property
    def priority(self):
        return 0

    @_Operator.handle_callables
    def binary(self, x, y):
        return x - y

    def unary(self, x):
        return -x


class _Mul(_Operator):

    SYMBOL = "*"

    @property
    def priority(self):
        return 10

    @_Operator.handle_callables
    def binary(self, x, y):
        return x * y

    def unary(self, x):
        super(_Mul, self).unary(x)


class _Div(_Operator):

    SYMBOL = "/"

    @property
    def priority(self):
        return 10

    @_Operator.handle_callables
    def binary(self, x, y):
        return x / y

    def unary(self, x):
        super(_Div, self).unary(x)


class _Pow(_Operator):

    SYMBOL = "^"

    @property
    def priority(self):
        return 20

    @_Operator.handle_callables
    def binary(self, x, y):
        return x ** y

    def unary(self, x):
        super(_Pow, self).unary(x)

