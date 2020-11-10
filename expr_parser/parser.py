from expr_parser.tokens import tokenize as _tokenize
from expr_parser.build_tree import _process_scope


class Parser:

    def __init__(self):
        self.brackets = {
            "(": ")",
            "[": "]"
        }

    def _is_opening_bracket(self, string: str) -> bool:
        return string in self.brackets.keys()

    def _is_closing_bracket(self, string: str) -> bool:
        return string in self.brackets.values()

    def _is_brackets(self, string: str) -> bool:
        return self._is_opening_bracket(string) or self._is_closing_bracket(string)

    def _group(self, tokens, process_scope=lambda x: x):
        """
        Group a stream of tokens into groups/scopes by brackets
        """
        result = []
        stack = []
        scope = result

        for token in tokens:
            # Got a opening bracket
            if self._is_opening_bracket(token):

                # Push current scope and opening bracket on stack
                stack.append((token, scope))

                # Create and enter new scope
                scope.append([])
                scope = scope[-1]

            # Got a closing bracket
            elif self._is_closing_bracket(token):
                # Check if there are any open brackets to close
                if len(stack) == 0:
                    raise SyntaxError("Missing opening bracket")

                # Enter the outer scope and get the opening bracket being closed
                opening, scope = stack.pop()

                # Check if the opening bracket matches the closing one
                if self.brackets[opening] != token:
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

    def parse(self, expr: str):
        return self._group(_tokenize(expr), process_scope=_process_scope)
