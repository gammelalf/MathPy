from parse.tokens import tokenize as _tokenize
from parse.group import group as _group
from parse.tree import BinOp as _BinOp
from parse.tree import UnaryOp as _UnaryOp
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
        lst = lst[:index - 1] + [_BinOp(left, operator, right)] + lst[index + 2:]

    return lst[0]


def _new_process_scope(lst):
    def consume_operator(i):
        op = lst[i]
        if i+1 == len(lst) or isinstance(lst[i+1], _Operator):
            raise SyntaxError(f"Operator '{op}' is missing its operand")
        right = lst[i+1]

        if i > 0 and not isinstance(lst[i-1], _Operator):
            left = lst[i-1]
        else:
            left = None

        if left is None:
            return lst[:i] + [_UnaryOp(op, right)] + lst[i+2:]
        else:
            return lst[:i-1] + [_BinOp(left, op, right)] + lst[i+2:]

    while len(lst) > 1:
        if isinstance(lst[0], _Operator):
            index = 0
        else:
            index = 1

        while index + 2 < len(lst) \
                and isinstance(lst[index+2], _Operator) \
                and lst[index].priority < lst[index+2].priority:
            index += 2

        lst = consume_operator(index)

    return lst[0]


def parse(string):
    return _group(_tokenize(string), process_scope=_new_process_scope)


def evaluate(string):
    return parse(string).eval()


def function(string):
    tree_ = parse(string)
    return lambda x: tree_.eval(x=x)
