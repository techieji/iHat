from enum import Enum
from functools import reduce
from operator import mul, eq, attrgetter
from itertools import zip_longest
from math import sqrt
from fractions import Fraction

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

char_to_op = {
    '+': Operation.ADD,
    '-': Operation.SUB,
    '*': Operation.MUL,
    '/': Operation.DIV,
    '^': Operation.POW,
    '@': Operation.ROOT,
}

op_to_char = dict(map(reversed, char_to_op.items()))

class Expr:
    def __init__(self, operation, args):
        self.operation = operation
        self.args = list(args)

    def __str__(self):
        if self.is_static or self.is_variable:
            return str(self.args[0])
        else:
            return f'{op_to_char[self.operation]}({", ".join(map(str, self.args))})'

    def __repr__(self):
        return f'Expr<"{str(self)}">'

    def __eq__(self, other):
        return type(self) == type(other) and self.operation == other.operation and self.args == other.args

    @property
    def is_static(self): return self.operation == Operation.STATIC
    @property
    def is_variable(self): return self.operation == Operation.VAR
    @property
    def value(self): return self.args[0]

    def evaluate(self, namespace):
        if self.operation.value > 0:
            collapsed = [x.evaluate(namespace) for x in self.args]
            return op_to_fn[self.operation](*collapsed)
        elif self.is_static:
            return self.value
        elif self.is_variable:
            return namespace[self.value]

    def simplify(self):
        "Simple simplifications. Stuff like x + x => 2x is in reframe"
        if self.is_static or self.is_variable:
            return self
        args = [x.simplify() for x in self.args]
        self.args = []
        fn = op_to_fn[self.operation]
        if self.operation == Operation.ADD:
            acc = 0
        elif self.operation == Operation.SUB:
            acc = args[0].value if args[0].is_static else 0   # Diff procedure
        elif self.operation == Operation.MUL:
            acc = 1
        elif self.operation == Operation.DIV:
            acc = args[0].value if args[0].is_static else 1   # Diff procedure

        if self.operation in [Operation.ADD, Operation.MUL]:
            for x in args:
                if x.is_static: acc = fn(acc, x.value)
                else: self.args.append(x)
            self.args.append(Expr.static(acc))
        elif self.operation in [Operation.SUB, Operation.DIV]:
            for x in args[1:]:
                if x.is_static: acc = fn(acc, x.value)
                else: self.args.append(x)
            if not args[0].is_static:
                self.args = [args[0]] + self.args
                if self.operation == Operation.SUB:
                    self.args = self.args + [Expr.static(-acc)]
                elif self.operation == Operation.DIV:
                    self.args = self.args + [Expr.static(1/acc)]
            else:
                self.args = [Expr.static(acc)] + self.args
        elif all(x.is_static for x in args):  # Pow or root
            self.args = [Expr.static(fn(*map(attrgetter('value'), args)))]   # Will be processed by 2 lines below

        if len(self.args) == 1:
            return self.value
        else:
            return self

    @staticmethod
    def static(n):
        return Expr(Operation.STATIC, [n])

    @staticmethod
    def _quick_construct(l):
        if type(l) is str:
            return Expr(Operation.VAR, [l])
        elif type(l) is not list:
            return Expr(Operation.STATIC, [l])
        else:
            return Expr(char_to_op[l[0]], map(Expr._quick_construct, l[1:]))
