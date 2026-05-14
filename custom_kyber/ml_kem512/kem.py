"""ML-KEM-512 CCA2 KEM (FIPS 203 / PQClean-compatible layout)."""

from __future__ import annotations

import secrets

from . import indcpa
from .params import (
    CIPHERTEXTBYTES,
    INDCPA_PUBLICKEYBYTES,
    INDCPA_SECRETKEYBYTES,
    PUBLICKEYBYTES,
    SECRETKEYBYTES,
    SYMBYTES,
)
from .symmetric import hash_g, hash_h, rkprf


def _cmov(dst: bytearray, src: bytes, b: int) -> None:
    """Constant-time-ish selection: dst = src if b==1 else unchanged (for b in {0,1})."""
    m = -b & 0xFF
    for i in range(len(dst)):
        dst[i] ^= m & (dst[i] ^ src[i])


def _verify(a: bytes, b: bytes) -> int:
    r = 0
    for x, y in zip(a, b):
        r |= x ^ y
    return 1 if r != 0 else 0


def keypair_derand(coins: bytes) -> tuple[bytes, bytes]:
    if len(coins) != 2 * SYMBYTES:
        raise ValueError("coins must be 64 bytes")
    pk, sk_indcpa = indcpa.indcpa_keypair_derand(coins[:SYMBYTES])
    sk = bytearray(sk_indcpa + pk)
    hpk = hash_h(pk)
    sk.extend(hpk)
    sk.extend(coins[SYMBYTES : 2 * SYMBYTES])
    return pk, bytes(sk)


def generate_keypair() -> tuple[bytes, bytes]:
    return keypair_derand(secrets.token_bytes(2 * SYMBYTES))


def encapsulate_derand(pk: bytes, coins: bytes) -> tuple[bytes, bytes]:
    if len(pk) != PUBLICKEYBYTES:
        raise ValueError("bad public key length")
    if len(coins) != SYMBYTES:
        raise ValueError("coins must be 32 bytes")
    buf = bytearray(coins + hash_h(pk))
    kr = hash_g(bytes(buf))
    ct = indcpa.indcpa_enc(bytes(buf[:SYMBYTES]), pk, kr[SYMBYTES:])
    ss = kr[:SYMBYTES]
    return ct, ss


def encapsulate(pk: bytes) -> tuple[bytes, bytes]:
    return encapsulate_derand(pk, secrets.token_bytes(SYMBYTES))


def decapsulate(sk: bytes, ct: bytes) -> bytes:
    if len(sk) != SECRETKEYBYTES or len(ct) != CIPHERTEXTBYTES:
        raise ValueError("bad decapsulate lengths")

    sk_indcpa = sk[:INDCPA_SECRETKEYBYTES]
    pk = sk[INDCPA_SECRETKEYBYTES : INDCPA_SECRETKEYBYTES + INDCPA_PUBLICKEYBYTES]
    hpk_stored = sk[SECRETKEYBYTES - 2 * SYMBYTES : SECRETKEYBYTES - SYMBYTES]
    z = sk[SECRETKEYBYTES - SYMBYTES :]

    m = indcpa.indcpa_dec(ct, sk_indcpa)
    buf = bytearray(m + hpk_stored)
    kr = hash_g(bytes(buf))
    cmp_ct = indcpa.indcpa_enc(m, pk, kr[SYMBYTES:])
    fail = _verify(ct, cmp_ct)

    ss = bytearray(rkprf(z, ct))
    _cmov(ss, kr[:SYMBYTES], fail ^ 1)
    return bytes(ss)
