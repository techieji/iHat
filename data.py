import numpy as np
from sympy import *
import csv

def get_iris():
    with open('iris.data') as iris:
        _vs, *_data = list(csv.reader(iris))
        vs = symbols(_vs[:-1])               # Going to be used to actually evaluate a hypothesis
        entries = np.array([x[:-1] for x in _data], dtype=np.float32).T    # Removing class (meant for continuous data)
        data = dict(zip(vs, entries))
    return vs, entries, data