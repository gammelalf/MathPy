from parse.tokens import tokenize as _tokenize
from parse.group import group as _group
from parse.tree import Operation as _Operation
from parse.tree import Operator as _Operator


__all__ = [
    "parse",
    "evaluate",
    "function"
]


def _process_scope(lst):
    while len(lst) > 1:
        index = 1
        while index + 2 < len(lst) and lst[index].priority < lst[index+2].priority:
            index += 2

        left, operator, right = lst[index - 1:index + 2]
        lst = lst[:index - 1] + [_Operation(left, operator, right)] + lst[index + 2:]

    return lst[0]


def parse(string):
    return _group(_tokenize(string), process_scope=_process_scope)


def evaluate(string):
    return parse(string).eval()


def function(string):
    tree_ = parse(string)
    return lambda x: tree_.eval(x=x)
