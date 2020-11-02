class Representable:

    def __repr__(self):
        cls = self.__class__.__name__
        args = ", ".join(map(repr, self.__dict__.values()))

        return f"{cls}({args})"


class MetaFunction(type):

    REQUIRES = [
                "eval",
                "_derive",
                "_format"
            ]

    def __init__(cls, name, bases, dct):
        for key in MetaFunction.REQUIRES:
            if key not in dct:
                raise NotImplementedError(
                        f"Please implement the function {key} for the class {name}"
                    )

        super().__init__(name, bases, dct)


class Function(Representable, metaclass=MetaFunction):

    def eval(self, x):
        raise NotImplementedError()

    def __call__(self, x):
        return self.eval(x)

    def _derive(self):
        raise NotImplementedError()

    def derive(self):
        return self._derive()

    def _format(self):
        raise NotImplementedError()

    def __str__(self):
        return self._format().format(x="x")

    def __eq__(self, other):
        if not isinstance(self, type(other)) and not isinstance(other, type(self)):
            return False
        else:
            return self.__dict__ == other.__dict__

