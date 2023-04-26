from dataclasses import dataclass, field
from typing import Any, Hashable, Iterable
from math import log, ceil

@dataclass(order=True)
class container:
    assessment: float
    expr: Any = field(compare=False)

class bloom:
    def __init__(self, b, k=3):
        self.ba = bytearray(b)
        self.bitlen = b * 8
        self.k = k

    def _set_bit(self, n, v):
        n = n % self.bitlen
        self.ba[n // 8] ^= v << (n % 8)

    def _get_bit(self, n):
        n = n % self.bitlen
        return (self.ba[n // 8] >> (n % 8)) % 2

    @staticmethod
    def _split_hash(h, k):
        h = abs(h) + 1
        l = ceil(log(h, 2))   # bit length
        step = l // k
        if step == 0:
            yield h
            return
        prev = 0
        for i in range(1, k):
            mv = i * step
            prev = h - (h >> mv << mv) - prev
            yield prev

    def __contains__(self, k):
        return all(map(self._get_bit, bloom._split_hash(hash(k), self.k)))

    def add(self, item):
        for x in bloom._split_hash(hash(item), self.k):
            self._set_bit(x, 1)

def unique(i: Iterable[Hashable]):
    b = bloom(100)
    for x in i:
        if x not in b:
            b.add(x)
            yield x
