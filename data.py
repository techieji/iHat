import numpy as np
from numpy.random import default_rng
from sympy import *
import csv
from random import randint
from typing import Callable

rng = default_rng()

def get_iris():
    with open('iris.data') as iris:
        _vs, *_data = list(csv.reader(iris))
        vs = symbols(_vs[:-1])               # Going to be used to actually evaluate a hypothesis
        entries = np.array([x[:-1] for x in _data], dtype=np.float32).T    # Removing class (meant for continuous data)
        data = dict(zip(vs, entries))
    return vs, entries, data

def from_function(fn: Callable[..., np.ndarray], output_sym: Symbol, ranges: dict[Symbol, tuple[float, float]], datasize=210, error=True):
    syms = ranges.keys()
    errors = rng.normal(size=datasize) if error else np.zeros(datasize)
    _entries = [rng.uniform(lower, upper, size=datasize) for lower, upper in ranges.values()]
    res = fn(*_entries) + errors
    entries = np.row_stack(_entries + [res])
    vs = list(syms) + [output_sym]
    data = dict(zip(vs, entries))
    return vs, entries, data

def from_csv(source: str, columns: list[Symbols]):
    with open(source) as data:
        _vs, *_data = list(csv.reader(data))
        vs = symbols(_vs[:-1])
        entries = np.array([x for x in _data], dtype=np.float32, ).T
        data = dict(zip(vs, entries))
    return vs, entries, data

def fake_force_data(datasize=210):
    a, m, F = symbols('a m F')
    return from_function(lambda a, m: a * m, F, {a: (0, 20), m: (1, 100)})

if __name__ == '__main__':
    print(fake_force_data()[1].shape)
    print(_fake_force_data()[1].shape)