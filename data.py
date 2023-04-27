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
        # _vs, *_data = iris |> csv.reader |> list
        vs = symbols(_vs[:-1])               # Going to be used to actually evaluate a hypothesis
        entries = np.array([x[:-1] for x in _data], dtype=np.float32).T    # Removing class (meant for continuous data)
        data = dict(zip(vs, entries))
    return vs, entries, data

def _fake_force_data(datasize=210):     # a = F/m    =>    F = ma
    _masses = [randint(10, 100) for _ in range(3)]
    masses = np.empty(datasize)
    size = datasize//2
    masses[0:size] = _masses[0]
    masses[size:2*size] = _masses[1]
    masses[2*size:3*size] = _masses[2]
    force = rng.integers(low=100, high=1000, size=datasize)
    acceleration = force/masses + rng.normal(size=datasize)/10
    vs = symbols('m F a')
    entries = np.array([masses, force, acceleration])
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

def fake_force_data(datasize=210):
    a, m, F = symbols('a m F')
    return from_function(lambda a, m: a * m, F, {a: (0, 20), m: (1, 100)})

if __name__ == '__main__':
    print(fake_force_data()[1].shape)
    print(_fake_force_data()[1].shape)