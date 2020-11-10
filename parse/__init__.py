from parse.tokens import tokenize as _tokenize
from parse.group import group as _group
from parse.tree import Operation as _Operation
from parse.tree import Operator as _Operator


__all__ = [
    "parse",
    "evaluate",
    "function"
]


# TODO bad runtime ~O(n^2)
def _process_scope(lst):
    while len(lst) > 1:
        # Find the highest priority operator
        index, priority = 0, float("-inf")
        for i, item in enumerate(lst):
            if not isinstance(item, _Operator):
                continue
            else:
                if priority < item.priority:
                    index, priority = i, item.priority

        left, operator, right = lst[index-1:index+2]
        lst = lst[:index-1] + [_Operation(left, operator, right)] + lst[index+2:]

    return lst[0]


def parse(string):
    return _group(_tokenize(string), process_scope=_process_scope)


def evaluate(string):
    return parse(string).eval()


def function(string):
    tree_ = parse(string)
    return lambda x: tree_.eval(x=x)
