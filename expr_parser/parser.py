import re as _re

from expr_parser.build_tree import _process_scope
from expr_parser.tree import Operator as _Operator
from expr_parser.tree import Var as _Var
from expr_parser.tree import Const as _Const


class Parser:

    def __init__(self):
        self.brackets = {
            "(": ")",
            "[": "]"
        }

        self.operators = {
        }

    def add_operator(self, operator: _Operator):
        self.operators[operator.SYMBOL] = operator

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
        return self._group(self._tokenize_with_implicit(expr), process_scope=_process_scope)


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
