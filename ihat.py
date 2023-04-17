from sympy import *
from itertools import chain
import numpy as np
import heapq

from data import get_iris, fake_force_data
from utils import container

np.seterr(all="ignore")
init_printing()

vs, entries, data = fake_force_data()

dv = symbols('a')           # Trying to predict petal length
using = symbols('m F')     # Using sepal length and width

def get_all_mutations(expr):   # Very simple for now
    for x in using:
        yield expr + x
        yield expr - x
        yield expr * x
        yield expr / x

def assess(expr):       # Lower is better
    f = lambdify(vs, expr, "numpy")
    o = f(*entries)
    accuracy   = np.nanvar(data[dv] / o) + np.nanvar(o / data[dv])
    complexity = sum(map(expr.count, vs))
    return accuracy + complexity**2

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