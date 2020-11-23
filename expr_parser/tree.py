from typing import (TypeVar as _TypeVar,
                    Dict as _Dict,
                    Set as _Set,
                    Union as _Union)

from expr_parser.operators.base import Operator as _Operator
from expr_parser.error import MissingVariable


_Numeric = _TypeVar("_Numeric", int, float, complex)


class Tree:

    __slots__ = ["root", "initial_namespace"]

    def __init__(self, root: "_Node", initial_namespace=None):
        self.root = root
        if initial_namespace is None:
            self.initial_namespace = {}
        else:
            self.initial_namespace = initial_namespace

    def _get_effective_namespace(self, namespace: _Dict):
        return dict(self.initial_namespace, **namespace)

    @property
    def used_variables(self):
        return self.root.used_variables

    def eval(self, **namespace: _Numeric) -> _Numeric:
        namespace = self._get_effective_namespace(namespace)
        for var in self.used_variables:
            if var not in namespace:
                raise MissingVariable(var)
        return self.root._eval(namespace)

    def simplified(self, **namespace: _Numeric) -> "Tree":
        namespace = self._get_effective_namespace(namespace)
        root = self.root._eval_partial(namespace)
        if isinstance(root, _Node):
            return Tree(root)
        else:
            return Tree(Constant(root))

    def __call__(self) -> _Numeric:
        return self.eval()


class _Node:

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        raise NotImplementedError()

    def _eval_partial(self, namespace: _Dict[str, _Numeric]) -> _Union["_Node", _Numeric]:
        raise NotImplementedError()

    @property
    def used_variables(self) -> _Set[str]:
        raise NotImplementedError()

    def _is_none(self) -> bool:
        """
        Overwritten in Constant to check if it's internal value is None.

        Operation uses this function to determine if it's a unary or binary operation.
        """
        return False


class Operation(_Node):

    __slots__ = ["operator", "x", "y"]

    def __init__(self, operator: _Operator, x: _Node, y: _Node = None):
        self.operator = operator
        self.x = x
        if y is None:
            self.y = Constant(None)
        else:
            self.y = y
        self._used_variables = self.x.used_variables | self.y.used_variables

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        x = self.x._eval(namespace)
        y = self.y._eval(namespace)

        return self.operator(x, y)

    def _eval_partial(self, namespace: _Dict[str, _Numeric]) -> _Union[_Node, _Numeric]:
        x = self.x._eval_partial(namespace)
        y = self.y._eval_partial(namespace)

        if not isinstance(x, _Node) and not isinstance(y, _Node):
            return self.operator(x, y)
        if not isinstance(x, _Node):
            x = Constant(x)
        if not isinstance(y, _Node):
            y = Constant(y)
        return Operation(self.operator, x, y)

    @property
    def used_variables(self) -> _Set[str]:
        return self._used_variables

    def __repr__(self):
        return f"Operation({self.operator}, {repr(self.x)}, {repr(self.y)})"

    def __str__(self):
        if self.y._is_none():
            return f"({self.operator} {self.x})"
        else:
            return f"({self.x} {self.operator} {self.y})"


class Constant(_Node):

    __slots__ = ["value"]

    def __init__(self, value: _Numeric):
        self.value = value

    def _is_none(self):
        return self.value is None

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        return self.value

    def _eval_partial(self, namespace: _Dict[str, _Numeric]) -> _Union[_Node, _Numeric]:
        return self.value

    @property
    def used_variables(self) -> _Set[str]:
        return set()

    def __repr__(self):
        return f"Const({repr(self.value)})"

    def __str__(self):
        return str(self.value)


class Variable(_Node):

    __slots__ = ["name"]

    def __init__(self, name: str):
        self.name = name

    def _eval(self, namespace: _Dict[str, _Numeric]) -> _Numeric:
        if self.name in namespace:
            return namespace[self.name]
        else:
            raise MissingVariable(self.name)

    def _eval_partial(self, namespace: _Dict[str, _Numeric]) -> _Union[_Node, _Numeric]:
        try:
            return self._eval(namespace)
        except MissingVariable:
            return Variable(self.name)

    @property
    def used_variables(self) -> _Set[str]:
        return {self.name}

    def __repr__(self):
        return f"Var({repr(self.name)})"

    def __str__(self):
        return str(self.name)


def tree_from_list(lst):
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
            return lst[:i] + [Operation(op, right)] + lst[i+2:]
        else:
            return lst[:i-1] + [Operation(op, left, right)] + lst[i + 2:]

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
