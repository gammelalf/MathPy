from random import randint

from parse.tree import Operator


class Dice(Operator):

    SYMBOL = "d"

    @property
    def priority(self):
        return 100

    def __call__(self, x, y):
        return sum((randint(1, y) for i in range(x)))
