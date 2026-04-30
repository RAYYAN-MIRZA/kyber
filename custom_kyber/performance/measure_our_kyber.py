"""
Benchmark script for the custom Kyber implementation.

This module measures the performance of the custom simplified Kyber implementation.
"""

import time
import sys
from pathlib import Path
from typing import Dict

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from custom_kyber.config import BENCHMARK_MESSAGE_BYTES, ETA1, ETA2, K, N, Q
from custom_kyber.kyber import keygen, encrypt, decrypt
from custom_kyber.utils import message_to_poly, poly_to_message


BENCHMARK_MESSAGE = bytes(range(BENCHMARK_MESSAGE_BYTES))


def benchmark_keygen(iterations: int = 100) -> float:
    """
    Benchmark custom Kyber key generation.
    
    Args:
        iterations: Number of iterations to run
        
    Returns:
        Average time in milliseconds
    """
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        keygen()
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    return sum(times) / len(times)


def benchmark_encrypt(iterations: int = 100) -> float:
    """
    Benchmark custom Kyber encryption.
    
    Args:
        iterations: Number of iterations to run
        
    Returns:
        Average time in milliseconds
    """
    public_key, _ = keygen()
    message_poly = message_to_poly(BENCHMARK_MESSAGE)
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        encrypt(public_key, message_poly)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    return sum(times) / len(times)


def benchmark_decrypt(iterations: int = 100) -> float:
    """
    Benchmark custom Kyber decryption.
    
    Args:
        iterations: Number of iterations to run
        
    Returns:
        Average time in milliseconds
    """
    public_key, secret_key = keygen()
    message_poly = message_to_poly(BENCHMARK_MESSAGE)
    ciphertext = encrypt(public_key, message_poly)
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        decrypt(secret_key, ciphertext)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    return sum(times) / len(times)


def get_our_kyber_timings(iterations: int = 100) -> Dict[str, float]:
    """
    Get benchmark timings for all custom Kyber operations.
    
    Args:
        iterations: Number of iterations per operation
        
    Returns:
        Dictionary with timing results in milliseconds
    """
    print("Benchmarking Custom Kyber Implementation...")
    print(f"  Parameters: n={N}, q={Q}, k={K}, eta1={ETA1}, eta2={ETA2}")
    print(f"  Input size: {BENCHMARK_MESSAGE_BYTES} bytes")
    print(f"  Running {iterations} iterations per operation...")
    
    keygen_time = benchmark_keygen(iterations)
    print(f"  KeyGen:  {keygen_time:.4f} ms")
    
    encrypt_time = benchmark_encrypt(iterations)
    print(f"  Encrypt: {encrypt_time:.4f} ms")
    
    decrypt_time = benchmark_decrypt(iterations)
    print(f"  Decrypt: {decrypt_time:.4f} ms")
    
    return {
        "KeyGen": keygen_time,
        "Encrypt": encrypt_time,
        "Decrypt": decrypt_time,
    }


if __name__ == "__main__":
    timings = get_our_kyber_timings(iterations=100)
    print("\nCustom Kyber Results:")
    for operation, time_ms in timings.items():
        print(f"  {operation}: {time_ms:.4f} ms")
