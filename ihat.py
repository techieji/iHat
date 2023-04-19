from sympy import *
from itertools import chain, islice
import numpy as np
import heapq
from typing import Iterable, Any

from data import get_iris, fake_force_data, rng
from utils import container
from eqrepr import expr
from math import nan

np.seterr(all="ignore")
init_printing()

vs, entries, data = fake_force_data()
dv = symbols('F')           # Trying to predict petal length
using = symbols('m a')     # Using sepal length and width

def assess(expr):       # Lower is better
    f = expr.vectorized
    o = f(*entries)
    expr = expr.sympy_expr
    accuracy     = np.nanvar(data[dv] / o) + np.nanvar(o / data[dv])
    try:
        completeness = sum(min(expr.count(v), 1) for v in vs)
        complexity   = sum(map(expr.count, vs))
    except AttributeError:
        completeness = 0
        complexity   = 0
    v = accuracy + max(complexity - completeness, 0)**2
    if v == nan:
        return np.inf
    return v

gen: Iterable[Any] = [expr.empty(vs, 10, using)]
temp_store: list[container] = []
for _ in range(20):     # Number of generations
    for expr in gen:
        v = assess(expr)
        if not np.isnan(v):
            heapq.heappush(temp_store, container(assess(expr), expr))
    l = [x.expr for x in temp_store[:10]]
    # l = list(islice((x.expr for x in temp_store if x.assessment != nan or x.assessment != np.nan), 10))
    print(temp_store[0].assessment, type(temp_store[0].assessment))
    gen = chain(l, chain.from_iterable(x.get_n_mutations(10, rng) for x in l))
    temp_store = []
print(l)

# m, a = symbols('m a')
# print(assess(m*a))