# Requirements: sympy, numpy

from sympy import *
from itertools import chain
import numpy as np
import heapq

from data import get_iris
from utils import container

np.seterr(all="ignore")
init_printing()

vs, entries, data = get_iris()

dv = symbols('pl')           # Trying to predict petal length
using = symbols('sl sw')     # Using sepal length and width

def get_all_mutations(expr):   # Very simple for now
    for x in using:
        yield expr + x
        yield expr - x
        yield expr * x
        yield expr / x

def assess(expr):       # Lower is better
    f = lambdify(vs, expr, "numpy")
    o = f(*entries)
    acc = np.nanvar(data[dv] / o) + np.nanvar(o / data[dv])
    return v

gen = [Integer(1)]
temp_store = []
for _ in range(5):     # Number of generations
    for expr in gen:
        heapq.heappush(temp_store, container(assess(expr), expr))
    l = [x.expr for x in temp_store[:10]]
    print(temp_store[0].assessment)
    gen = chain(l, chain.from_iterable(map(get_all_mutations, l)))
    temp_store = []
print(l)