from enum import Enum
from functools import reduce
from operator import mul, eq
from itertools import zip_longest
from math import sqrt

class Operation(Enum):
    ADD  = 1
    SUB  = 2
    MUL  = 3
    DIV  = 4
    POW  = 101     # Test for 2-arged operators: `op > 100`
    ROOT = 102     # square root
    STATIC = -1    # Test for special operators: `op < 0`
    VAR = -2

op_to_fn = {
    Operation.ADD: lambda *a: sum(a),
    Operation.SUB: lambda *a: a[0] - sum(a[1:]),
    Operation.MUL: lambda *a: reduce(mul, a),
    Operation.DIV: lambda *a: a[0] / reduce(mul, a),
    Operation.POW: lambda a, b: a**b,
    Operation.ROOT: lambda a: sqrt(a)
}

class Expr:
    def __init__(self, operation: Operation, args: list):
        self.operation = operation
        self.args = list(args)

    @property
    def is_static(self) -> bool: return self.operation == Operation.STATIC
    @property
    def is_variable(self) -> bool: return self.operation == Operation.VAR
    @property
    def value(self): return self.args[0]

    def evaluate(self, namespace: dict) -> int:
        if self.operation.value > 0:
            collapsed = [x.evaluate(namespace) for x in self.args]
            return op_to_fn[self.operation](*collapsed)
        elif self.is_static:
            return self.value
        elif self.is_variable:
            return namespace[self.value]

    def simplify(self) -> 'Expr':
        "Simple simplifications. Stuff like x + x => 2x is in reframe"
        if self.is_static or self.is_variable:
            return self
        args = [x.simplify() for x in self.args]
        self.args = []
        fn = op_to_fn(self.operation)
        if self.operation.value < 5:
            acc = self.value.value if self.value.is_static else 0
            for x in self.args:
                if x.is_static: acc = fn(acc, x.value)
                else: self.args.append(x)
            self.args.append(Expr.static(acc))
        elif all(x.is_static for x in self.args):  # Pow or root
            self.args = [Expr.static(op_to_fn(*self.args))]
        if len(self.args) == 1:
            return self.value
        else:
            return self

    @staticmethod
    def static(n: int) -> 'Expr':
        return Expr(Operation.STATIC, [n])

    @staticmethod
    def _quick_construct(l: list) -> 'Expr':
        if type(l) != list:
            if type(l) == str:
                return Expr(Operation.VAR, [l])
            else:
                return Expr(Operation.STATIC, [l])
        if l[0] == '+':
            return Expr(Operation.ADD, map(Expr._quick_construct, l[1:]))
        elif l[0] == '-':
            return Expr(Operation.SUB, map(Expr._quick_construct, l[1:]))
        elif l[0] == '*':
            return Expr(Operation.MUL, map(Expr._quick_construct, l[1:]))
        elif l[0] == '/':
            return Expr(Operation.DIV, map(Expr._quick_construct, l[1:]))
        elif l[0] == '^':
            return Expr(Operation.POW, map(Expr._quick_construct, l[1:]))
        elif l[0] == '@':
            return Expr(Operation.ROOT, map(Expr._quick_construct, l[1:]))

    def __eq__(self, other):
        return type(self) == type(other) and self.operation == other.operation and self.args == other.args
