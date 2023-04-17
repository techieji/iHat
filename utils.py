from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class container:
    assessment: float
    expr: Any = field(compare=False)

class var_counter:
    def __init__(self, v=1):
        self.v = v

    def __repr__(self): return f"var_counter({self.v})"
    def __str__(self):  return f"var_counter({self.v})"

    def _prototype(self, other):
        if type(other) == type(self):
            return var_counter(self.v + other.v)
        return self

for x in dir(int):
    if x.startswith('__') and x not in dir(var_counter):
        setattr(var_counter, x, var_counter._prototype)