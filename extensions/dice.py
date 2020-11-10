from random import randint

from parse.tree import Operator


class Dice(Operator):

    SYMBOL = "d"

    @property
    def priority(self):
        return 100

    def binary(self, x, y):
        return sum((randint(1, y) for i in range(x)))

    def unary(self, x):
        return randint(1, x)
