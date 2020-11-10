import re

from parse.tree import Operator, Const, Var


__numeric_re = re.compile(r"^(\d+)?(\.\d*)?( ?i)?$")


def _is_numeric(string):
    return __numeric_re.match(string) is not None


def _parse_numeric_const(string) -> Const:
    match = __numeric_re.match(string)
    if match is None:
        raise ValueError(f"'{string}' is not a compatible numeric")
    leading, decimals, imaginary = match.groups()

    # A decimal dot without leading digits
    if decimals and not leading:
        leading = "0"

    # Single i without leading or decimal digits
    if imaginary and not leading:
        leading = "1"

    if imaginary:
        if decimals:
            return Const(complex(leading+decimals+"j"))
        else:
            return Const(complex(leading+"j"))
    elif decimals:
        return Const(float(leading+decimals))
    else:
        return Const(int(leading))


BRACKETS = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">"
        }


def _is_bracket(string):
    return string in BRACKETS.keys() or string in BRACKETS.values()


def tokenize(string: str):
    def is_valid_token(s: str):
        return _is_numeric(s) or _is_bracket(s) or Operator.is_operator(s) or s.isidentifier()

    def create_token(s: str):
        if _is_bracket(s):
            return s
        elif Operator.is_operator(s):
            return Operator.get(s)
        elif s.isidentifier():
            return Var(s)
        elif _is_numeric(s):
            return _parse_numeric_const(s)
        else:
            raise ValueError(f"Unknown token: '{s}'")

    token = ""
    for char in string:
        if char == " ":
            if token != "":
                yield create_token(token)
                token = ""
        elif is_valid_token(token+char):
            token += char
        else:
            yield create_token(token)
            token = char

    if token != "":
        yield create_token(token)
