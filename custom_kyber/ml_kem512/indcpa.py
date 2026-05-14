"""CPA public-key encryption core (ML-KEM-512 / Kyber512)."""

from __future__ import annotations

from copy import deepcopy

from .params import (
    INDCPA_BYTES,
    INDCPA_MSGBYTES,
    INDCPA_PUBLICKEYBYTES,
    INDCPA_SECRETKEYBYTES,
    K,
    N,
    POLYCOMPRESSEDBYTES,
    POLYVECBYTES,
    POLYVECCOMPRESSEDBYTES,
    Q,
    SYMBYTES,
    XOF_BLOCKBYTES,
)
from . import polynomial as poly
from .symmetric import hash_g, xof_shake128_blocks


def _rej_uniform(buf: bytes, length: int) -> tuple[list[int], int]:
    """Return (coeffs mod q, bytes_consumed) or partial coeffs if buf too short."""
    r: list[int] = []
    pos = 0
    while len(r) < length and pos + 3 <= len(buf):
        val0 = (buf[pos] | (buf[pos + 1] << 8)) & 0xFFF
        val1 = ((buf[pos + 1] >> 4) | (buf[pos + 2] << 4)) & 0xFFF
        pos += 3
        if val0 < Q:
            r.append(val0)
        if len(r) < length and val1 < Q:
            r.append(val1)
    return r, pos


def _gen_matrix(seed: bytes, transposed: bool) -> list[list[list[int]]]:
    """K×K matrix of polynomials (time domain coeffs), matching PQ-Crystals gen_matrix."""
    gen_nblocks = ((12 * N // 8) * (1 << 12) // Q + XOF_BLOCKBYTES) // XOF_BLOCKBYTES
    mat: list[list[list[int]]] = [[poly.poly_zero() for _ in range(K)] for _ in range(K)]

    for i in range(K):
        for j in range(K):
            x, y = (i, j) if transposed else (j, i)
            xof = xof_shake128_blocks(seed, x, y)
            buf = b"".join(next(xof) for _ in range(gen_nblocks))
            coeffs, _ = _rej_uniform(buf, N)
            while len(coeffs) < N:
                buf = next(xof)
                more, _ = _rej_uniform(buf, N - len(coeffs))
                coeffs.extend(more)
            mat[i][j] = coeffs[:N]
    return mat


def indcpa_keypair_derand(coins: bytes) -> tuple[bytes, bytes]:
    if len(coins) != SYMBYTES:
        raise ValueError("coins must be 32 bytes")
    buf = bytearray(coins)
    buf.append(K)
    buf = bytearray(hash_g(bytes(buf[: SYMBYTES + 1])))
    publicseed = bytes(buf[:SYMBYTES])
    noiseseed = bytes(buf[SYMBYTES:])

    a_mat = _gen_matrix(publicseed, transposed=False)

    skpv = [poly.poly_getnoise_eta1(noiseseed, n) for n in range(K)]
    e = [poly.poly_getnoise_eta1(noiseseed, K + n) for n in range(K)]

    skpv_ntt = deepcopy(skpv)
    e_ntt = deepcopy(e)
    poly.polyvec_ntt(skpv_ntt)
    poly.polyvec_ntt(e_ntt)

    pkpv = [poly.poly_zero() for _ in range(K)]
    for i in range(K):
        poly.polyvec_basemul_acc_montgomery(pkpv[i], a_mat[i], skpv_ntt)
        poly.poly_tomont(pkpv[i])
    poly.polyvec_add(pkpv, pkpv, e_ntt)
    poly.polyvec_reduce(pkpv)

    sk_bytes = poly.polyvec_tobytes(skpv_ntt)
    pk_bytes = poly.polyvec_tobytes(pkpv) + publicseed
    return pk_bytes, sk_bytes


def indcpa_enc(
    m: bytes,
    pk: bytes,
    coins: bytes,
) -> bytes:
    if len(m) != INDCPA_MSGBYTES or len(pk) != INDCPA_PUBLICKEYBYTES or len(coins) != SYMBYTES:
        raise ValueError("bad indcpa_enc input lengths")

    pkpv = poly.polyvec_frombytes(pk[:POLYVECBYTES])
    seed = pk[POLYVECBYTES : POLYVECBYTES + SYMBYTES]
    k_poly = poly.poly_frommsg(m)

    at = _gen_matrix(seed, transposed=True)

    nonce = 0
    sp = [poly.poly_getnoise_eta1(coins, nonce + i) for i in range(K)]
    nonce += K
    ep = [poly.poly_getnoise_eta2(coins, nonce + i) for i in range(K)]
    nonce += K
    epp = poly.poly_getnoise_eta2(coins, nonce)

    sp_ntt = deepcopy(sp)
    poly.polyvec_ntt(sp_ntt)

    b = [poly.poly_zero() for _ in range(K)]
    for i in range(K):
        poly.polyvec_basemul_acc_montgomery(b[i], at[i], sp_ntt)

    v = poly.poly_zero()
    poly.polyvec_basemul_acc_montgomery(v, pkpv, sp_ntt)

    poly.polyvec_invntt_tomont(b)
    poly.poly_invntt_tomont(v)

    poly.polyvec_add(b, b, ep)
    poly.poly_add(v, v, epp)
    poly.poly_add(v, v, k_poly)
    poly.polyvec_reduce(b)
    poly.poly_reduce(v)

    return poly.polyvec_compress(b) + poly.poly_compress(v)


def indcpa_dec(c: bytes, sk: bytes) -> bytes:
    if len(c) != INDCPA_BYTES or len(sk) != INDCPA_SECRETKEYBYTES:
        raise ValueError("bad indcpa_dec input lengths")

    b = poly.polyvec_decompress(c[:POLYVECCOMPRESSEDBYTES])
    v = poly.poly_decompress(c[POLYVECCOMPRESSEDBYTES : POLYVECCOMPRESSEDBYTES + POLYCOMPRESSEDBYTES])
    skpv = poly.polyvec_frombytes(sk)

    b_ntt = deepcopy(b)
    poly.polyvec_ntt(b_ntt)

    mp = poly.poly_zero()
    poly.polyvec_basemul_acc_montgomery(mp, skpv, b_ntt)
    poly.poly_invntt_tomont(mp)

    poly.poly_sub(mp, v, mp)
    poly.poly_reduce(mp)
    return poly.poly_tomsg(mp)
