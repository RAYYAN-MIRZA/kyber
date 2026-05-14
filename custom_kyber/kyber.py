"""
ML-KEM-512 (Kyber-512) key encapsulation — bytes in/out, shared secret for symmetric crypto.

This module wraps the from-scratch implementation in ``custom_kyber.ml_kem512``.
"""

from __future__ import annotations

from custom_kyber.ml_kem512 import (
    CIPHERTEXTBYTES,
    PUBLICKEYBYTES,
    SECRETKEYBYTES,
    SSBYTES,
    decapsulate,
    encapsulate,
    encapsulate_derand,
    generate_keypair,
    keypair_derand,
)

__all__ = [
    "CIPHERTEXTBYTES",
    "PUBLICKEYBYTES",
    "SECRETKEYBYTES",
    "SSBYTES",
    "generate_keypair",
    "keypair_derand",
    "encapsulate",
    "encapsulate_derand",
    "decapsulate",
]
