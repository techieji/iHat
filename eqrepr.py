# Expression representation (stack based)

from enum import Enum
from collections import namedtuple
from math import sqrt
import operator as op
import random as rd
import itertools as it
import numpy as np
from functools import cached_property, partial
from sympy import lambdify, symbols
from sympy.core.symbol import Symbol

class INS(Enum):
    LOAD_CONST = 0
    LOAD_VAR   = 1
    ADD = op.add
    SUB = op.sub
    MUL = op.mul
    DIV = op.truediv
    POW = pow
    SQRT = 7

ALL_INS_TYPES = list(map(partial(getattr, INS), filter(str.isupper, dir(INS))))

Ins = namedtuple('Ins', 'ins arg')     # Arg is used by load_const and load_var with index

def get_random_ins(const_bound: int, vs: list[Symbol]) -> Ins:
    t = rd.choice(ALL_INS_TYPES)
    match t:
        case INS.LOAD_CONST:
            return Ins(t, rd.randint(0, const_bound))
        case INS.LOAD_VAR:
            return Ins(t, rd.choice(vs))
        case _:
            return Ins(t, None)

class expr:     # Immutable
    def __init__(self, inses, constants, vs: tuple[Symbol]):
        self.inses = list(inses)
        self.constants = constants if type(constants) is np.ndarray else np.array(constants)
        self.vars = vs

    @cached_property
    def const_len(self):
        return len(self.constants)
    
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
        while not (w := self._get_raw_mutation(rng)).valid: pass
        return w

    def _get_raw_mutation(self, rng=np.random):
        inses = self.inses + [get_random_ins(self.const_len, self.vs)] if rd.random() < 0.1 else self.inses    # TODO: parametrize
        try:
            # Not shuffle bc we want it to be similar
            inses = next(x for x in it.permutations(inses) if rd.random() < 0.1)   # TODO: Change threshold to depend on length
        except StopIteration:
            shuffle(inses)
        constants = self.constants + rng.normal(size=len(self.constants))
        return expr(inses, constants, self.vars)

    @cached_property
    def to_expr(self):
        return self.eval(self.vars)

    @cached_property
    def vectorized(self):
        return lambdify(self.vars, self.to_expr(), "numpy")