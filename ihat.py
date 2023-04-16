# Requirements: sympy, numpy

from sympy import *
from itertools import chain
from dataclasses import dataclass, field
from typing import Any       # If I didn't have to, I wouldn't
import numpy as np
import csv
import heapq

np.seterr(all="ignore")


from pprint import pprint

with open('iris.data') as iris:
    _vs, *_data = list(csv.reader(iris))
    vs = symbols(_vs[:-1])               # Going to be used to actually evaluate a hypothesis
    entries = np.array([x[:-1] for x in _data], dtype=np.float32).T    # Removing class (meant for continuous data)
    data = dict(zip(vs, entries))

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
    v = np.nanvar(data[dv] / o) + np.nanvar(o / data[dv])
    return v

@dataclass(order=True)
class container:
    assessment: float
    expr: Any = field(compare=False)

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