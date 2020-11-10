BRACKETS = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">"
        }


def group(tokens, process_scope=lambda x: x):
    result = []
    stack = []
    scope = result

    for token in tokens:
        # Got a opening bracket
        if token in BRACKETS.keys():

            # Push current scope and opening bracket on stack
            stack.append((token, scope))

            # Create and enter new scope
            scope.append([])
            scope = scope[-1]

        # Got a closing bracket
        elif token in BRACKETS.values():
            # Check if there are any open brackets to close
            if len(stack) == 0:
                raise SyntaxError("Missing opening bracket")

            # Enter the outer scope and get the opening bracket being closed
            opening, scope = stack.pop()

            # Check if the opening bracket matches the closing one
            if BRACKETS[opening] != token:
                raise SyntaxError("Got missmatching brackets")

            # Process just finished scope
            scope[-1] = process_scope(scope[-1])

        # Got no bracket
        else:
            scope.append(token)

    # Check if all brackets have been closed
    if len(stack) > 0:
        raise SyntaxError("Missing closing bracket")

    # Process and returned finished outest scope
    return process_scope(result)


def tee(x):
    """
    Testing function imitating the tee command

    It prints its input and returns it
    """
    print(x)
    return x

