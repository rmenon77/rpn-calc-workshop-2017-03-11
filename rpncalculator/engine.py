try:
    from inspect import signature as funcsignature
except ImportError:
    from funcsigs import signature as funcsignature

from .errors import DuplicateOperationError
from .errors import InvalidOperationSignatureError
from .errors import InvalidValueTypeError


def noop(engine): return


class Engine(object):

    def __init__(self):
        self._stack = []
        self._operations = {'noop': noop}

    def pop(self):
        if len(self._stack) == 0:
            return None
        return self._stack.pop()

    def push(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise InvalidValueTypeError()
        self._stack.append(value)
        return value

    def execute(self, operation):
        self._operations[operation](engine=self)
        return self._stack[-1]

    def register(self, operation, function):
        signature = funcsignature(function)
        if (
                len(signature.parameters) != 1
                or 'engine' not in signature.parameters
                ):
            raise InvalidOperationSignatureError()
        if operation in self._operations:
            raise DuplicateOperationError()
        self._operations[operation] = function