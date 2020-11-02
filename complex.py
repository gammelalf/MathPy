from base import Function


class KoeffFunc(Function):
    """
    g(x) = k * f(x)
    """

    def __init__(self, coeff, func):
        self.k = coeff
        self.f = func

    def _derive(self):
        return KoeffFunc(self.k, self.f._derive())

    def eval(self, x):
        return self.k * self.f(x)

    def _format(self):
        return f"{str(self.k)}({self.f._format()})"


class SumFunc(Function):
    """
    g(x) = f1(x) + f2(x) + f3(x) + ...
    """

    def __init__(self, *funcs):
        self.fs = funcs

    def _derive(self):
        return SumFunc(*tuple(map(lambda f: f._derive(), self.fs)))

    def eval(self, x):
        return sum(map(lambda f: f(x), self.fs))

    def _format(self):
        return " + ".join(map(lambda f: f._format(), self.fs))


def prod(iterable, /, start=1):
    """
    Return the product of a 'start' value (default: 1) times an iterable of numbers

    When the iterable is empty, return the start value.
    This function is intended specifically for use with numeric values and may
    reject non-numeric types.
    """
    end = start
    for i in iterable:
        end *= i
    return end



class ProdFunc(Function):
    """
    g(x) = f1(x) * f2(x) * f3(x) * ...
    """

    def __init__(self, *funcs):
        self.fs = list(funcs)

    def _derive(self):
        def function(i, j):
            if i == j:
                return self.fs[j]._derive()
            else:
                return self.fs[j]

        n = len(self.fs)

        return SumFunc(*[
                    ProdFunc(*[
                        function(i, j)
                        for j in range(n)
                    ])
                    for i in range(n)
                ])


    def eval(self, x):
        return prod(map(lambda f: f(x), self.fs))

    def _format(self):
        return " * ".join(map(lambda f: f._format(), self.fs))


class CompFunc(Function):

    def __init__(self, outer, inner):
        self.g = outer
        self.h = inner

    def _derive(self):
        return ProdFunc(CompFunc(self.g._derive(), self.h), self.h._derive())

    def eval(self, x):
        return self.g(self.f(x))

    def _format(self):
        return self.g._format().format(x=f"({self.h._format()})")

