"""Centered binomial sampling (Kyber reference)."""

from __future__ import annotations

from .params import N, Q


def _load32_le(x: bytes, off: int) -> int:
    return int.from_bytes(x[off : off + 4], "little")


def _load24_le(x: bytes, off: int) -> int:
    return int.from_bytes(x[off : off + 3], "little")


def cbd2(buf: bytes) -> list[int]:
    assert len(buf) == 2 * N // 4
    r = [0] * N
    for i in range(N // 8):
        t = _load32_le(buf, 4 * i)
        d = t & 0x55555555
        d += (t >> 1) & 0x55555555
        for j in range(8):
            a = (d >> (4 * j + 0)) & 0x3
            b = (d >> (4 * j + 2)) & 0x3
            r[8 * i + j] = a - b
    return r


def cbd3(buf: bytes) -> list[int]:
    assert len(buf) == 3 * N // 4
    r = [0] * N
    for i in range(N // 4):
        t = _load24_le(buf, 3 * i)
        d = t & 0x00249249
        d += (t >> 1) & 0x00249249
        d += (t >> 2) & 0x00249249
        for j in range(4):
            a = (d >> (6 * j + 0)) & 0x7
            b = (d >> (6 * j + 3)) & 0x7
            r[4 * i + j] = a - b
    return r


def poly_cbd_eta1(buf: bytes, eta1: int) -> list[int]:
    if eta1 == 2:
        return cbd2(buf)
    if eta1 == 3:
        return cbd3(buf)
    raise ValueError("eta1 must be 2 or 3")


def poly_cbd_eta2(buf: bytes) -> list[int]:
    return cbd2(buf)
