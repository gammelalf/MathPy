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

I try to make the parsing as modular as possible.

Currently this means it is very easy to use custom operators:

### Custom Operators

A custom operator can be created by subclassing `expr_parser.tree.Operator` and providing the following:

- `SYMBOL`: class constant containing the operator's string representation
- `priority`: object attribute for determening the operation's execution order
- `binary`: object method (optional) for using the operator between two values x and y
- `unary`: object method (optional) for using the operator in front of a single value x

The `Operator` class provides the `@Operator.handle_callables` decorator to extend the binary method to work with functions as well as numbers.

```python
from expr_parser.tree import Operator

class Modulo(Operator):

  SYMBOL = "%"

  @property
  def priority(self):
    return 20

  @Operator.handle_callables
  def binary(self, left, right):
    return left % right
```

Just by creating the class, it will be registered and usable.

The basic math operators +, -, *, /, ^ are implemented in `expr_parser.operators.basic`.
Since the classes just need to be declared in order to register a operator.
Importing this file will register them.

In `expr_parser.operators.dice` is another example for a custom operator.
It's the dice operator known from tabletop-roleplays,
where `2d6` means roll a 6-sided die 2-times.
