"""
Comparison script for Custom Kyber vs Reference Kyber512.

This script runs both implementations and collects their timing data.
"""

from typing import Dict, Tuple

from custom_kyber.performance.measure_our_kyber import get_our_kyber_timings


def get_reference_timings(iterations: int = 100) -> Dict[str, float]:
    """
    Get benchmark timings from reference Kyber512.
    
    Args:
        iterations: Number of iterations per operation
        
    Returns:
        Dictionary with timing results in milliseconds, or None if unavailable
    """
    try:
        from reference_kyber.kyber_reference import get_reference_timings as ref_timings
        timings = ref_timings(iterations)
        return timings
    except ImportError as e:
        print(f"⚠ Reference Kyber is unavailable, skipping comparison")
        print(f"  ImportError: {e}")
        return None
    except RuntimeError as e:
        print(f"⚠ Reference Kyber is unavailable, skipping comparison")
        print(f"  RuntimeError: {e}")
        return None
    except Exception as e:
        print(f"⚠ Reference Kyber is unavailable, skipping comparison")
        print(f"  Error: {type(e).__name__}: {e}")
        return None

def compare_implementations(iterations: int = 100) -> Tuple[Dict, Dict]:
    """
    Compare custom Kyber implementation with reference Kyber512.
    
    Args:
        iterations: Number of iterations per operation
        
    Returns:
        Tuple of (our_timings, reference_timings)
    """
    print("=" * 60)
    print("Kyber Implementation Comparison Benchmark")
    print("=" * 60)
    print()
    
    # Benchmark custom implementation
    our_timings = get_our_kyber_timings(iterations)
    print()
    
    # Benchmark reference implementation
    reference_timings = get_reference_timings(iterations)
    
    if reference_timings is None:
        print("Skipping reference Kyber comparison (pqcrypto not installed)")
        return our_timings, None
    
    print()
    print("=" * 60)
    print("Comparison Results")
    print("=" * 60)
    print()
    print(f"{'Operation':<15} {'Custom (ms)':<15} {'Reference (ms)':<15} {'Ratio':<10}")
    print("-" * 60)
    
    for operation in ["KeyGen", "Encrypt", "Decrypt"]:
        our_time = our_timings[operation]
        ref_time = reference_timings[operation]
        ratio = our_time / ref_time
        
        print(f"{operation:<15} {our_time:<15.4f} {ref_time:<15.4f} {ratio:<10.2f}x")
    
    print()
    
    return our_timings, reference_timings


def print_summary(our_timings: Dict, reference_timings: Dict):
    """
    Print a summary of the comparison.
    
    Args:
        our_timings: Timings from custom implementation
        reference_timings: Timings from reference implementation
    """
    if reference_timings is None:
        print("Summary: Only custom implementation was benchmarked.")
        total_our = sum(our_timings.values())
        print(f"Total time (all operations): {total_our:.4f} ms")
        return
    
    total_our = sum(our_timings.values())
    total_ref = sum(reference_timings.values())
    overall_ratio = total_our / total_ref
    
    print("Summary:")
    print(f"  Custom Implementation Total: {total_our:.4f} ms")
    print(f"  Reference Implementation Total: {total_ref:.4f} ms")
    print(f"  Overall Ratio: {overall_ratio:.2f}x")
    print()
    
    if overall_ratio > 1:
        print(f"  Note: Custom implementation is {overall_ratio:.2f}x slower than reference.")
        print("  This is expected for a scratch educational implementation using naive polynomial multiplication.")
    else:
        print(f"  Note: Custom implementation is {1/overall_ratio:.2f}x faster than reference.")
        print("  This can happen because the custom code is still an educational PKE-style model,")
        print("  while pqcrypto runs the full ML-KEM-512 KEM with production serialization and checks.")


if __name__ == "__main__":
    iterations = 100
    our_timings, reference_timings = compare_implementations(iterations)
    
    if reference_timings:
        print_summary(our_timings, reference_timings)
