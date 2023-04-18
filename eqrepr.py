# Expression representation (to replace sympy) (stack based)

from enum import Enum
from collections import namedtuple
from math import sqrt
import operator as op
import random as rd
import itertools as it
import numpy as np

class INS(Enum):
    LOAD_CONST = 0
    LOAD_VAR   = 1
    ADD = op.add
    SUB = op.sub
    MUL = op.mul
    DIV = op.truediv
    POW = pow
    SQRT = 7

Ins = namedtuple('Ins', 'ins arg')     # Arg is used by load_const and load_var with index

class expr:
    def __init__(self, inses, constants, vs):
        self.inses = inses
        self.constants = constants if type(constants) is np.ndarray else np.array(constants)
        self.vars = vs
    
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
                    stack.append(ins.ins.value(stack.pop(), stack.pop()))    # Yeah, it's reversed, ig
        return stack.pop()

    @property
    def valid(self):     # O(n)
        sc = 0
        for ins in self.inses:
            match ins.ins:
                case INS.LOAD_CONST | INS.LOAD_VAR:
                    sc += 1
                case INS.SQRT:
                    None
                case _:
                    sc -= 1
            if sc < 0:
                return False
        return True

    def get_mutation(self, rng=np.random):
        while True:
            try:
                reorder = next(x for x in it.permutations(self.inses) if rd.random() < 0.1)
                break
            except StopIteration:
                continue
        constants = self.constants + rng.normal(size=len(self.constants))
        return expr(reorder, constants, self.vars)