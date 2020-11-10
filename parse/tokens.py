import re

from parse.tree import Operator, Const, Var


__numeric_re = re.compile(r"^(\d+)?(\.\d*)?( ?i)?$")


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


def tokenize(string):
    unused = ""

    def consume_char(c: str):
        if Operator.is_operator(c):
            return Operator.get(c)
        elif c in BRACKETS.keys() or c in BRACKETS.values():
            return c

    def consume_string(s: str):
        if s != "i" and s.isidentifier():
            return Var(s)
        else:
            return _parse_numeric_const(s)

    for char in string.replace(" ", ""):
        token = consume_char(char)

        if token is None:
            unused += char
        else:
            if unused != "":
                yield consume_string(unused)
                unused = ""
            yield token

    if unused != "":
        yield consume_string(unused)
