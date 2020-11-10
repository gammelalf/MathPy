from expr_parser.parser import Parser
from expr_parser.operators import basic


__all__ = [
    "Parser",
    "parse",
    "evaluate",
    "function"
]


_default_parser = Parser()
for op in [basic._Implicit, basic._Add, basic._Sub, basic._Mul, basic._Div, basic._Pow]:
    _default_parser.add_operator(op())


def parse(expr: str):
    return _default_parser.parse(expr)


def evaluate(expr: str):
    return parse(expr).eval()


def function(expr: str):
    tree = parse(expr)
    return lambda x: tree.eval(x=x)
