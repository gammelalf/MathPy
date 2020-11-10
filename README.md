# MathPy
A small parser for arithmetic expressions

The goal is to parse expressions like `(1+2)*3` and evaluate them.

It also parses an identifiers like `x+2`.
The resulting object then needs values for those to evaluate itself.

## CLI

The package can be executed as script.
It will evaluate an expression and accepts any number of key-value-pairs to use for variables.

```bash
~$ python3 -m expr_parser x^2+y x=2 y=1
5
```

## Basic Usage

The main API provides 3 functions (each takes an expression):

- `parse` as the name says, parses the expression an returns a syntax tree
- `evaluate` creates and immidiently evaluates the resulting syntax tree. No unknown can be used!
- `function` takes an expression containing the unknown `x` and returns a function

```python
>>> from expr_parser import *
>>> evaluate("(1+2)*3")
9
>>> f = function("x^2")
>>> f(4)
16
```

## Advanced Usage

### The Parser object

The basic API is just a shortcut for instancing a Parser object and calling its methods.

A Parser object contains the information required for parsing an expression:
- What brackets are used
- Which operators are used

These can be controled with:
- `Parser.add_brackets(opening, closing)`
- `Parser.add_operator(operator)`

The static method `default()` instances an object and populates it with the default brackets and operators.
This method is used to provide the basic API's parser.

### Custom Operators

An operator object requires the following parameters:

- `symbol`: sthe operator's string representation
- `priority`: integer for determening the operation's execution order
- `binary`: method for using the operator between two values x and y
- `unary`: method for using the operator in front of a single value x

The `Operator` class provides the `@Operator.handle_callables` decorator to extend the binary method to work with functions as well as numbers.

```python
from expr_parser.operators.base import Operator

Mod = Operator(
  symbol="%",
  priority=20
  binary=Operator.handle_callables(lambda x, y: x % y)
)
```

The basic math operators +, -, *, /, ^ are implemented in `expr_parser.operators.default`.

In `expr_parser.operators.dice` is another example for a custom operator.
It's the dice operator known from tabletop-roleplays,
where `2d6` means roll a 6-sided die 2-times.
