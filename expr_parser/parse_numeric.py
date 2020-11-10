import re

from expr_parser.tree import Const


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
            return Const(complex(leading + decimals + "j"))
        else:
            return Const(complex(leading + "j"))
    elif decimals:
        return Const(float(leading + decimals))
    else:
        return Const(int(leading))
