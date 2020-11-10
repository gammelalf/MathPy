from expr_parser.parser import Parser
from expr_parser.operators import default


__all__ = [
    "Parser",
    "parse",
    "evaluate",
    "function"
]


_default_parser = Parser.default()


def parse(expr: str):
    return _default_parser.parse(expr)


def evaluate(expr: str):
    return parse(expr).eval()


def function(expr: str):
    tree = parse(expr)
    return lambda x: tree.eval(x=x)
