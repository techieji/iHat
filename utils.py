from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class container:
    assessment: float
    expr: Any = field(compare=False)