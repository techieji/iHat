from sympy import *
from itertools import chain
import numpy as np
import heapq
from typing import Iterable, Any

from data import get_iris, fake_force_data
from utils import container

np.seterr(all="ignore")
init_printing()

vs, entries, data = fake_force_data()
dv = symbols('F')           # Trying to predict petal length
using = symbols('m a')     # Using sepal length and width

def get_all_mutations(expr):   # Very simple for now
    for x in using:
        yield expr + x
        yield expr - x
        yield expand(expr * x)
        yield expand(expr / x)

def assess(expr):       # Lower is better
    f = lambdify(vs, expr, "numpy")
    o = f(*entries)
    accuracy     = np.nanvar(data[dv] / o) + np.nanvar(o / data[dv])
    completeness = sum(min(expr.count(v), 1) for v in vs)
    complexity   = sum(map(expr.count, vs))
    return accuracy + max(complexity - completeness, 0)**2

gen: Iterable[Any] = [*using]
temp_store: list[container] = []
for _ in range(10):     # Number of generations
    for expr in gen:
        heapq.heappush(temp_store, container(assess(expr), expr))
    l = [x.expr for x in temp_store[:10]]
    print(temp_store[0].assessment)
    gen = chain(l, chain.from_iterable(map(get_all_mutations, l)))
    temp_store = []
print(l)

m, a = symbols('m a')
print(assess(m*a))