import numpy as np
from numpy.random import default_rng
from sympy import *
import csv
from random import randint

rng = default_rng()

def get_iris():
    with open('iris.data') as iris:
        _vs, *_data = list(csv.reader(iris))
        vs = symbols(_vs[:-1])               # Going to be used to actually evaluate a hypothesis
        entries = np.array([x[:-1] for x in _data], dtype=np.float32).T    # Removing class (meant for continuous data)
        data = dict(zip(vs, entries))
    return vs, entries, data

def fake_force_data(datasize=210):     # a = F/m    =>    F = ma
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

if __name__ == '__main__':
    print(fake_force_data()[2])