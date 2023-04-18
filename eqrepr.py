# Expression representation (to replace sympy) (stack based)

from enum import Enum
from collection import namedtuple
from math import sqrt
import operator as op

class INS(Enum):
    LOAD_CONST = 0
    LOAD_VAR   = 1
    ADD = op.add
    SUB = op.sub
    MUL = op.mul
    DIV = op.truediv
    POW = pow
    SQRT = 7

Ins = namedtuple('ins', 'ins arg')     # Arg is used by load_const and load_var with index

class expr:
    def __init__(self, inses, constants, vars):
        self.inses = inses
        self.constants = constants
        self.vars = vars
    
    def eval(self, *args):             # Simple, dirty, and dumb way of doing it
        vs = dict(zip(self.vars, args))
        stack = []
        for ins in self.inses:
            match ins.ins:
                case INS.LOAD_CONST:
                    stack.append(self.constants[ins.arg])
                case INS.LOAD_VAR:
                    stack.append(vs[ins.arg])
                case INS.SQRT:
                    stack.append(sqrt(stack.pop()))
                case _:
                    stack.append(ins.ins(stack.pop(), stack.pop()))    # Yeah, it's reversed, ig
        return stack.pop()