import sys

from expr_parser import evaluate, parse


def main(args):
    if len(args) < 2:
        print(f"Usage: {args[0]} <EXPRESSION> [<KEY>=<VALUE> ...]")
        print(f"")
        print(f"This program evaluates a arithmetic expression.")
        print(f"Any number of key-value-pairs can be given to use for variables:")
        print(f"    {args[0]} x^2+y x=2 y=1")
        print(f"    5")
        exit(1)
    elif len(args) == 2:
        print(evaluate(args[1]))
    else:
        namespace = dict((
            (key, evaluate(value))
            for key, value in map(
                lambda x: x.split("="),
                args[2:]
            )
        ))
        print(parse(args[1]).eval(**namespace))
    exit(0)


if __name__ == "__main__":
    main(sys.argv)
