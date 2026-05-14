"""Polynomial and polynomial-vector operations for ML-KEM-512."""

from __future__ import annotations

from . import cbd
from .params import (
    ETA1,
    ETA2,
    K,
    N,
    POLYBYTES,
    POLYCOMPRESSEDBYTES,
    POLYVECBYTES,
    POLYVECCOMPRESSEDBYTES,
    Q,
)
from .reduce_ops import barrett_reduce, montgomery_reduce
from .ntt import invntt_tomont, ntt, poly_basemul_montgomery
from .symmetric import prf


def poly_zero() -> list[int]:
    return [0] * N


def poly_reduce(p: list[int]) -> None:
    for i in range(N):
        p[i] = barrett_reduce(p[i])


def poly_add(r: list[int], a: list[int], b: list[int]) -> None:
    for i in range(N):
        r[i] = a[i] + b[i]


def poly_sub(r: list[int], a: list[int], b: list[int]) -> None:
    for i in range(N):
        r[i] = a[i] - b[i]


def poly_ntt(r: list[int]) -> None:
    ntt(r)
    poly_reduce(r)


def poly_invntt_tomont(r: list[int]) -> None:
    invntt_tomont(r)


def poly_tomont(r: list[int]) -> None:
    f = pow(2, 32, Q)
    for i in range(N):
        r[i] = montgomery_reduce(r[i] * f)


def poly_tobytes(a: list[int]) -> bytes:
    out = bytearray(POLYBYTES)
    for i in range(N // 2):
        t0 = a[2 * i] + ((a[2 * i] >> 15) & Q)
        t1 = a[2 * i + 1] + ((a[2 * i + 1] >> 15) & Q)
        t0 &= 0xFFF
        t1 &= 0xFFF
        out[3 * i + 0] = t0 & 0xFF
        out[3 * i + 1] = (t0 >> 8) | ((t1 & 0x0F) << 4)
        out[3 * i + 2] = t1 >> 4
    return bytes(out)


def poly_frombytes(data: bytes) -> list[int]:
    assert len(data) == POLYBYTES
    r = poly_zero()
    for i in range(N // 2):
        r[2 * i] = data[3 * i] | ((data[3 * i + 1] & 0xFF) << 8)
        r[2 * i] &= 0xFFF
        r[2 * i + 1] = (data[3 * i + 1] >> 4) | (data[3 * i + 2] << 4)
        r[2 * i + 1] &= 0xFFF
    return r


def poly_compress(a: list[int]) -> bytes:
    out = bytearray(POLYCOMPRESSEDBYTES)
    pos = 0
    for i in range(N // 8):
        t = [0] * 8
        for j in range(8):
            u = a[8 * i + j]
            u += (u >> 15) & Q
            d0 = u << 4
            d0 += 1665
            d0 *= 80635
            d0 >>= 28
            t[j] = d0 & 0xF
        out[pos + 0] = t[0] | (t[1] << 4)
        out[pos + 1] = t[2] | (t[3] << 4)
        out[pos + 2] = t[4] | (t[5] << 4)
        out[pos + 3] = t[6] | (t[7] << 4)
        pos += 4
    return bytes(out)


def poly_decompress(data: bytes) -> list[int]:
    assert len(data) == POLYCOMPRESSEDBYTES
    r = poly_zero()
    for i in range(N // 2):
        r[2 * i + 0] = (((data[i] & 15) * Q) + 8) >> 4
        r[2 * i + 1] = (((data[i] >> 4) * Q) + 8) >> 4
    return r


def poly_frommsg(msg: bytes) -> list[int]:
    assert len(msg) == N // 8
    r = poly_zero()
    for i in range(32):
        for j in range(8):
            bit = (msg[i] >> j) & 1
            r[8 * i + j] = ((Q + 1) // 2) if bit else 0
    return r


def poly_tomsg(a: list[int]) -> bytes:
    msg = bytearray(32)
    for i in range(32):
        for j in range(8):
            t = a[8 * i + j]
            t <<= 1
            t += 1665
            t *= 80635
            t >>= 28
            t &= 1
            msg[i] |= t << j
    return bytes(msg)


def poly_getnoise_eta1(seed: bytes, nonce: int) -> list[int]:
    buf = prf(ETA1 * N // 4, seed, nonce)
    return cbd.poly_cbd_eta1(buf, ETA1)


def poly_getnoise_eta2(seed: bytes, nonce: int) -> list[int]:
    buf = prf(ETA2 * N // 4, seed, nonce)
    return cbd.poly_cbd_eta2(buf)


def polyvec_zero() -> list[list[int]]:
    return [poly_zero() for _ in range(K)]


def polyvec_ntt(r: list[list[int]]) -> None:
    for i in range(K):
        poly_ntt(r[i])


def polyvec_invntt_tomont(r: list[list[int]]) -> None:
    for i in range(K):
        poly_invntt_tomont(r[i])


def polyvec_reduce(r: list[list[int]]) -> None:
    for i in range(K):
        poly_reduce(r[i])


def polyvec_add(r: list[list[int]], a: list[list[int]], b: list[list[int]]) -> None:
    for i in range(K):
        poly_add(r[i], a[i], b[i])


def polyvec_basemul_acc_montgomery(r: list[int], a: list[list[int]], b: list[list[int]]) -> None:
    t = poly_zero()
    poly_basemul_montgomery(r, a[0], b[0])
    for i in range(1, K):
        poly_basemul_montgomery(t, a[i], b[i])
        poly_add(r, r, t)
    poly_reduce(r)


def polyvec_tobytes(a: list[list[int]]) -> bytes:
    return b"".join(poly_tobytes(a[i]) for i in range(K))


def polyvec_frombytes(data: bytes) -> list[list[int]]:
    assert len(data) == POLYVECBYTES
    return [poly_frombytes(data[i * POLYBYTES : (i + 1) * POLYBYTES]) for i in range(K)]


def polyvec_compress(a: list[list[int]]) -> bytes:
    out = bytearray(POLYVECCOMPRESSEDBYTES)
    pos = 0
    for i in range(K):
        for j in range(N // 4):
            t = [0] * 4
            for k in range(4):
                v = a[i][4 * j + k]
                v += (v >> 15) & Q
                d0 = v << 10
                d0 += 1665
                d0 *= 1290167
                d0 >>= 32
                t[k] = d0 & 0x3FF
            out[pos + 0] = t[0] & 0xFF
            out[pos + 1] = (t[0] >> 8) | ((t[1] & 0x3F) << 2)
            out[pos + 2] = (t[1] >> 6) | ((t[2] & 0x0F) << 4)
            out[pos + 3] = (t[2] >> 4) | ((t[3] & 0x03) << 6)
            out[pos + 4] = t[3] >> 2
            pos += 5
    return bytes(out)


def polyvec_decompress(data: bytes) -> list[list[int]]:
    assert len(data) == POLYVECCOMPRESSEDBYTES
    r = polyvec_zero()
    pos = 0
    for i in range(K):
        for j in range(N // 4):
            t0 = data[pos + 0] | (data[pos + 1] << 8)
            t1 = (data[pos + 1] >> 2) | (data[pos + 2] << 6)
            t2 = (data[pos + 2] >> 4) | (data[pos + 3] << 4)
            t3 = (data[pos + 3] >> 6) | (data[pos + 4] << 2)
            pos += 5
            r[i][4 * j + 0] = ((t0 & 0x3FF) * Q + 512) >> 10
            r[i][4 * j + 1] = ((t1 & 0x3FF) * Q + 512) >> 10
            r[i][4 * j + 2] = ((t2 & 0x3FF) * Q + 512) >> 10
            r[i][4 * j + 3] = ((t3 & 0x3FF) * Q + 512) >> 10
    return r
