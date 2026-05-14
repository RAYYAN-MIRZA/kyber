# config.py — shared constants for benchmarks and docs.

Q = 3329
N = 256
K = 2

ETA1 = 3
ETA2 = 2

NOISE_MIN = -ETA2
NOISE_MAX = ETA2

BENCHMARK_MESSAGE_BYTES = 32

# ML-KEM-512 / Kyber512 byte sizes (see custom_kyber.ml_kem512.params)
from custom_kyber.ml_kem512.params import (  # noqa: E402
    CIPHERTEXTBYTES,
    PUBLICKEYBYTES,
    SECRETKEYBYTES,
    SSBYTES,
)

__all__ = [
    "Q",
    "N",
    "K",
    "ETA1",
    "ETA2",
    "NOISE_MIN",
    "NOISE_MAX",
    "BENCHMARK_MESSAGE_BYTES",
    "PUBLICKEYBYTES",
    "SECRETKEYBYTES",
    "CIPHERTEXTBYTES",
    "SSBYTES",
]
