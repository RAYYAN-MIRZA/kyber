"""Barrett and Montgomery reduction (Kyber reference semantics)."""

from __future__ import annotations

from .params import Q

QINV = (-3327) & 0xFFFF  # 62209


def _int16(x: int) -> int:
    x &= 0xFFFF
    if x >= 0x8000:
        x -= 0x10000
    return x


def montgomery_reduce(a: int) -> int:
    t = _int16((a * QINV) & 0xFFFF)
    u = (a - t * Q) >> 16
    return _int16(u & 0xFFFF)


def barrett_reduce(a: int) -> int:
    v = ((1 << 26) + Q // 2) // Q
    t = (v * a + (1 << 25)) >> 26
    t *= Q
    return a - t


def fqmul(a: int, b: int) -> int:
    return montgomery_reduce(a * b)
