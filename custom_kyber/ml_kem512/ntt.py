"""Number-theoretic transform for R_q = Z_q[X]/(X^256+1), q=3329."""

from __future__ import annotations

from .params import Q
from .reduce_ops import barrett_reduce, fqmul, montgomery_reduce

# From PQ-Crystals Kyber ref/ntt.c
ZETAS = (
    -1044, -758, -359, -1517, 1493, 1422, 287, 202,
    -171, 622, 1577, 182, 962, -1202, -1474, 1468,
    573, -1325, 264, 383, -829, 1458, -1602, -130,
    -681, 1017, 732, 608, -1542, 411, -205, -1571,
    1223, 652, -552, 1015, -1293, 1491, -282, -1544,
    516, -8, -320, -666, -1618, -1162, 126, 1469,
    -853, -90, -271, 830, 107, -1421, -247, -951,
    -398, 961, -1508, -725, 448, -1065, 677, -1275,
    -1103, 430, 555, 843, -1251, 871, 1550, 105,
    422, 587, 177, -235, -291, -460, 1574, 1653,
    -246, 778, 1159, -147, -777, 1483, -602, 1119,
    -1590, 644, -872, 349, 418, 329, -156, -75,
    817, 1097, 603, 610, 1322, -1285, -1465, 384,
    -1215, -136, 1218, -1335, -874, 220, -1187, -1659,
    -1185, -1530, -1278, 794, -1510, -854, -870, 478,
    -108, -308, 996, 991, 958, -1460, 1522, 1628,
)


def ntt(r: list[int]) -> None:
    k = 1
    length = 128
    while length >= 2:
        start = 0
        while start < 256:
            zeta = ZETAS[k]
            k += 1
            for j in range(start, start + length):
                t = fqmul(zeta, r[j + length])
                r[j + length] = r[j] - t
                r[j] = r[j] + t
            start += 2 * length
        length >>= 1


def invntt_tomont(r: list[int]) -> None:
    k = 127
    length = 2
    while length <= 128:
        start = 0
        while start < 256:
            zeta = ZETAS[k]
            k -= 1
            for j in range(start, start + length):
                t = r[j]
                r[j] = barrett_reduce(t + r[j + length])
                r[j + length] = r[j + length] - t
                r[j + length] = fqmul(zeta, r[j + length])
            start += 2 * length
        length <<= 1

    f = 1441
    for j in range(256):
        r[j] = fqmul(r[j], f)


def basemul(a0: int, a1: int, b0: int, b1: int, zeta: int) -> tuple[int, int]:
    t0 = fqmul(a1, b1)
    t0 = fqmul(t0, zeta)
    t0 = t0 + fqmul(a0, b0)
    t1 = fqmul(a0, b1) + fqmul(a1, b0)
    return t0, t1


def poly_basemul_montgomery(r: list[int], a: list[int], b: list[int]) -> None:
    for i in range(64):
        z = ZETAS[64 + i]
        r[4 * i], r[4 * i + 1] = basemul(
            a[4 * i], a[4 * i + 1], b[4 * i], b[4 * i + 1], z
        )
        r[4 * i + 2], r[4 * i + 3] = basemul(
            a[4 * i + 2],
            a[4 * i + 3],
            b[4 * i + 2],
            b[4 * i + 3],
            -z,
        )
