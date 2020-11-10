from expr_parser.parser import Parser
import expr_parser.operators.basic


__all__ = [
    "Parser",
    "parse",
    "evaluate",
    "function"
]


def parse(expr: str):
    return Parser().parse(expr)


def evaluate(expr: str):
    return parse(expr).eval()


def function(expr: str):
    tree = parse(expr)
    return lambda x: tree.eval(x=x)
