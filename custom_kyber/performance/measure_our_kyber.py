"""
Benchmark script for the custom ML-KEM-512 (Kyber512) implementation.

Measures KeyGen, Encapsulate (Encrypt), and Decapsulate (Decrypt) in milliseconds.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Dict

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from custom_kyber.ml_kem512.params import (
    CIPHERTEXTBYTES,
    PUBLICKEYBYTES,
    SECRETKEYBYTES,
    SSBYTES,
)
from custom_kyber.kyber import decapsulate, encapsulate, generate_keypair


def benchmark_keygen(iterations: int = 100) -> float:
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        generate_keypair()
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return sum(times) / len(times)


def benchmark_encapsulate(iterations: int = 100) -> float:
    public_key, _ = generate_keypair()
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        encapsulate(public_key)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return sum(times) / len(times)


def benchmark_decapsulate(iterations: int = 100) -> float:
    public_key, secret_key = generate_keypair()
    ciphertext, _ = encapsulate(public_key)
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        decapsulate(secret_key, ciphertext)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return sum(times) / len(times)


def get_our_kyber_timings(iterations: int = 100) -> Dict[str, float]:
    print("Benchmarking Custom ML-KEM-512 Implementation...")
    print(
        f"  Sizes: pk={PUBLICKEYBYTES} B, sk={SECRETKEYBYTES} B, "
        f"ct={CIPHERTEXTBYTES} B, ss={SSBYTES} B"
    )
    print(f"  Running {iterations} iterations per operation...")

    keygen_time = benchmark_keygen(iterations)
    print(f"  KeyGen:  {keygen_time:.4f} ms")

    encrypt_time = benchmark_encapsulate(iterations)
    print(f"  Encrypt: {encrypt_time:.4f} ms")

    decrypt_time = benchmark_decapsulate(iterations)
    print(f"  Decrypt: {decrypt_time:.4f} ms")

    return {
        "KeyGen": keygen_time,
        "Encrypt": encrypt_time,
        "Decrypt": decrypt_time,
    }


if __name__ == "__main__":
    timings = get_our_kyber_timings(iterations=100)
    print("\nCustom ML-KEM-512 Results:")
    for operation, time_ms in timings.items():
        print(f"  {operation}: {time_ms:.4f} ms")
