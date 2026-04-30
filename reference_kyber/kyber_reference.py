"""Reference Kyber512 implementation using pqcrypto library.

This module provides a reference implementation of the standard ML-KEM/Kyber
for benchmarking purposes.

Requirements:
    pip install pqcrypto

Note: If pqcrypto is not available, install it with:
    pip install pqcrypto
"""

import time
from typing import Tuple, Dict

REFERENCE_PARAMETERS = {
    "algorithm": "ML-KEM-512",
    "n": 256,
    "q": 3329,
    "k": 2,
    "shared_secret_bytes": 32,
}

try:
    from pqcrypto.kem import ml_kem_512
except ImportError as e:
    print(f"DEBUG: Import failed with: {e}")
    ml_kem_512 = None
except Exception as e:
    print(f"DEBUG: Unexpected error during import: {e}")
    ml_kem_512 = None


class ReferenceKyber512:
    """Wrapper for standard Kyber512 implementation using pqcrypto."""
    
    def __init__(self):
        if ml_kem_512 is None:
            raise ImportError(
                "pqcrypto is not installed.\n"
                "Install it with: pip install pqcrypto"
            )
    
    def keygen(self) -> Tuple[bytes, bytes]:
        """
        Generate a Kyber512 keypair.
        
        Returns:
            Tuple of (public_key, secret_key)
        """
        public_key, secret_key = ml_kem_512.generate_keypair()
        return public_key, secret_key
    
    def encrypt(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """
        Perform Kyber512 encapsulation.
        
        Args:
            public_key: The recipient's public key
            
        Returns:
            Tuple of (ciphertext, shared_secret)
        """
        ciphertext, shared_secret = ml_kem_512.encrypt(public_key)
        return ciphertext, shared_secret
    
    def decrypt(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        """
        Perform Kyber512 decapsulation.
        
        Args:
            secret_key: The recipient's secret key
            ciphertext: The ciphertext to decrypt
            
        Returns:
            The decrypted shared secret
        """
        shared_secret = ml_kem_512.decrypt(secret_key, ciphertext)
        return shared_secret


def benchmark_keygen(iterations: int = 100) -> float:
    """
    Benchmark Kyber512 key generation.
    
    Args:
        iterations: Number of iterations to run
        
    Returns:
        Average time in milliseconds
    """
    try:
        kyber = ReferenceKyber512()
    except (ImportError, RuntimeError) as e:
        raise RuntimeError(f"Cannot benchmark reference Kyber: {e}") from e
    
    times = []
    
    for _ in range(iterations):
        try:
            start = time.perf_counter()
            kyber.keygen()
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms
        except Exception as e:
            raise RuntimeError(f"Error during keygen benchmark: {e}") from e
    
    return sum(times) / len(times)


def benchmark_encrypt(iterations: int = 100) -> float:
    """
    Benchmark Kyber512 encryption (encapsulation).
    
    Args:
        iterations: Number of iterations to run
        
    Returns:
        Average time in milliseconds
    """
    try:
        kyber = ReferenceKyber512()
        public_key, _ = kyber.keygen()
    except (ImportError, RuntimeError) as e:
        raise RuntimeError(f"Cannot benchmark reference Kyber: {e}") from e
    
    times = []
    
    for _ in range(iterations):
        try:
            start = time.perf_counter()
            kyber.encrypt(public_key)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms
        except Exception as e:
            raise RuntimeError(f"Error during encrypt benchmark: {e}") from e
    
    return sum(times) / len(times)


def benchmark_decrypt(iterations: int = 100) -> float:
    """
    Benchmark Kyber512 decryption (decapsulation).
    
    Args:
        iterations: Number of iterations to run
        
    Returns:
        Average time in milliseconds
    """
    try:
        kyber = ReferenceKyber512()
        public_key, secret_key = kyber.keygen()
        ciphertext, _ = kyber.encrypt(public_key)
    except (ImportError, RuntimeError) as e:
        raise RuntimeError(f"Cannot benchmark reference Kyber: {e}") from e
    
    times = []
    
    for _ in range(iterations):
        try:
            start = time.perf_counter()
            kyber.decrypt(secret_key, ciphertext)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms
        except Exception as e:
            raise RuntimeError(f"Error during decrypt benchmark: {e}") from e
    
    return sum(times) / len(times)


def get_reference_timings(iterations: int = 100) -> Dict[str, float]:
    """
    Get benchmark timings for all Kyber512 operations.
    
    Args:
        iterations: Number of iterations per operation
        
    Returns:
        Dictionary with timing results in milliseconds
        
    Raises:
        RuntimeError: If reference Kyber is not available
    """
    print("Benchmarking Reference Kyber512...")
    print(
        "  Parameters: "
        f"n={REFERENCE_PARAMETERS['n']}, "
        f"q={REFERENCE_PARAMETERS['q']}, "
        f"k={REFERENCE_PARAMETERS['k']}"
    )
    print(f"  Shared secret size: {REFERENCE_PARAMETERS['shared_secret_bytes']} bytes")
    print(f"  Running {iterations} iterations per operation...")
    
    try:
        keygen_time = benchmark_keygen(iterations)
        print(f"  KeyGen:  {keygen_time:.4f} ms")
    except RuntimeError as e:
        raise RuntimeError(f"KeyGen benchmark failed: {e}") from e
    
    try:
        encrypt_time = benchmark_encrypt(iterations)
        print(f"  Encrypt: {encrypt_time:.4f} ms")
    except RuntimeError as e:
        raise RuntimeError(f"Encrypt benchmark failed: {e}") from e
    
    try:
        decrypt_time = benchmark_decrypt(iterations)
        print(f"  Decrypt: {decrypt_time:.4f} ms")
    except RuntimeError as e:
        raise RuntimeError(f"Decrypt benchmark failed: {e}") from e
    
    return {
        "KeyGen": keygen_time,
        "Encrypt": encrypt_time,
        "Decrypt": decrypt_time,
    }

if __name__ == "__main__":
    try:
        timings = get_reference_timings(iterations=100)
        print("\nReference Kyber512 Results:")
        for operation, time_ms in timings.items():
            print(f"  {operation}: {time_ms:.4f} ms")
    except ImportError as e:
        print(f"Error: {e}")
