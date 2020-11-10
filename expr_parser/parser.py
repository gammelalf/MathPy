import re as _re
import math as _math
from typing import Dict as _Dict

from expr_parser.operators.base import Operator as _Operator
from expr_parser.tree import (Tree as _Tree,
                              Variable as _Var,
                              Constant as _Const,
                              tree_from_list as _tree_from_list)
from expr_parser.operators.default import (Implicit as _Implicit,
                                           Add as _Add,
                                           Sub as _Sub,
                                           Mul as _Mul,
                                           Div as _Div,
                                           Pow as _Pow)


class Parser:

    @staticmethod
    def default():
        parser = Parser()
        parser.add_bracket("(", ")")
        for op in (_Implicit, _Add, _Sub, _Mul, _Div, _Pow):
            parser.add_operator(op)
        parser.constants = {
            "pi": _math.pi,
            "e": _math.e,
            "i": 1j,

            "sin": _math.sin,
            "cos": _math.cos,
            "tan": _math.tan,
            "log": _math.log
        }
        return parser

    def __init__(self):
        self.brackets: _Dict[str, str] = {}
        self.operators: _Dict[str, _Operator] = {}
        self.constants: _Dict = {}

    def add_operator(self, operator: _Operator):
        self.operators[operator.symbol] = operator

    def add_bracket(self, opening, closing):
        self.brackets[opening] = closing

    def _is_opening_bracket(self, string: str) -> bool:
        return string in self.brackets.keys()

    def _is_closing_bracket(self, string: str) -> bool:
        return string in self.brackets.values()

    def _is_bracket(self, string: str) -> bool:
        return self._is_opening_bracket(string) or self._is_closing_bracket(string)

    def _is_operator(self, string: str) -> bool:
        return string in self.operators.keys()

    def _is_valid_token(self, s: str):
        return _is_numeric(s) or self._is_bracket(s) or self._is_operator(s) or s.isidentifier()

    def _create_token(self, s: str):
        if self._is_bracket(s):
            return s
        elif self._is_operator(s):
            return self.operators[s]
        elif s.isidentifier():
            return _Var(s)
        elif _is_numeric(s):
            return _parse_numeric_const(s)
        else:
            raise ValueError(f"Unknown token: '{s}'")

    def _tokenize(self, string: str):
        token = ""
        for char in string:
            if char == " ":
                if token != "":
                    yield self._create_token(token)
                    token = ""
            elif self._is_valid_token(token + char):
                token += char
            else:
                yield self._create_token(token)
                token = char

        if token != "":
            yield self._create_token(token)

    def _tokenize_with_implicit(self, string):
        iterator = self._tokenize(string)

        try:
            token = next(iterator)
        except StopIteration:
            return

        for next_token in iterator:
            yield token
            if isinstance(token, (_Const, _Var)) and (
                    isinstance(next_token, (_Const, _Var)) or self._is_opening_bracket(next_token)):
                yield self.operators["==IMPLICIT=="]
            token = next_token

        yield token

    def _group(self, tokens, process_scope=lambda x: x):
        """
        Group a stream of tokens into groups/scopes by brackets
        """
        result = []
        stack = []
        scope = result

        for token in tokens:
            # Got a opening bracket
            if self._is_opening_bracket(token):

                # Push current scope and opening bracket on stack
                stack.append((token, scope))

                # Create and enter new scope
                scope.append([])
                scope = scope[-1]

            # Got a closing bracket
            elif self._is_closing_bracket(token):
                # Check if there are any open brackets to close
                if len(stack) == 0:
                    raise SyntaxError("Missing opening bracket")

                # Enter the outer scope and get the opening bracket being closed
                opening, scope = stack.pop()

                # Check if the opening bracket matches the closing one
                if self.brackets[opening] != token:
                    raise SyntaxError("Got mismatching brackets")

                # Process just finished scope
                scope[-1] = process_scope(scope[-1])

            # Got no bracket
            else:
                scope.append(token)

        # Check if all brackets have been closed
        if len(stack) > 0:
            raise SyntaxError("Missing closing bracket")

        # Process and returned finished outermost scope
        return process_scope(result)

    def parse(self, expr: str):
        if self._is_operator("==IMPLICIT=="):
            root = self._group(self._tokenize_with_implicit(expr), process_scope=_tree_from_list)
        else:
            root = self._group(self._tokenize(expr), process_scope=_tree_from_list)
        return _Tree(root, self.constants)


__numeric_re = _re.compile(r"^(\d+)?(\.\d*)?$")


def _is_numeric(string):
    return __numeric_re.match(string) is not None and string != "."


def _parse_numeric_const(string) -> _Const:
    try:
        return _Const(int(string))
    except ValueError:
        pass
    try:
        return _Const(float(string))
    except ValueError:
        pass
    raise ValueError(f"'{string}' is neither an int or float")
