"""SHA-3 / SHAKE helpers matching Kyber symmetric.h (stdlib only)."""

from __future__ import annotations

import hashlib

from .params import CIPHERTEXTBYTES, SYMBYTES


def hash_h(data: bytes) -> bytes:
    return hashlib.sha3_256(data).digest()


def hash_g(data: bytes) -> bytes:
    return hashlib.sha3_512(data).digest()


def prf(out_len: int, key: bytes, nonce: int) -> bytes:
    assert len(key) == SYMBYTES
    h = hashlib.shake_256()
    h.update(key + bytes([nonce]))
    return h.digest(out_len)


def rkprf(key: bytes, inp: bytes) -> bytes:
    assert len(key) == SYMBYTES
    assert len(inp) == CIPHERTEXTBYTES
    h = hashlib.shake_256()
    h.update(key)
    h.update(inp)
    return h.digest(SYMBYTES)


def xof_shake128_blocks(seed: bytes, x: int, y: int):
    """SHAKE128(seed||x||y); yield 168-byte blocks (rate)."""
    assert len(seed) == SYMBYTES
    h = hashlib.shake_128()
    h.update(seed + bytes([x, y]))
    while True:
        yield h.digest(168)
