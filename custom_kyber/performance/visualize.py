"""
Visualization script for benchmark results.

This module generates bar charts comparing custom Kyber with reference Kyber512.

Requirements:
    pip install matplotlib
"""

import sys
from pathlib import Path
from typing import Dict, Optional
import json

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from custom_kyber.config import BENCHMARK_MESSAGE_BYTES, ETA1, ETA2, K, N, Q

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
except ImportError:
    matplotlib = None
    plt = None



def plot_comparison(
    our_timings: Dict[str, float],
    reference_timings: Optional[Dict[str, float]],
    output_path: str = None
) -> str:
    """
    Generate a bar chart comparing custom Kyber with reference Kyber512.
    
    Args:
        our_timings: Timings from custom implementation
        reference_timings: Timings from reference implementation (optional)
        output_path: Path to save the output image
        
    Returns:
        Path to the saved image file
    """
    if plt is None:
        raise ImportError(
            "matplotlib is not installed.\n"
            "Install it with: pip install matplotlib"
        )
    
    if output_path is None:
        output_path = str(
            Path(__file__).parent.parent / "report_assets" / "performance.png"
        )
    
    # Ensure output directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare data
    operations = list(our_timings.keys())
    our_values = [our_timings[op] for op in operations]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = range(len(operations))
    width = 0.35
    
    # Plot custom implementation
    bars1 = ax.bar(
        [i - width/2 for i in x],
        our_values,
        width,
        label='Custom Kyber (Simplified)',
        color='#FF6B6B',
        alpha=0.8
    )
    
    # Plot reference implementation if available
    if reference_timings:
        ref_values = [reference_timings[op] for op in operations]
        bars2 = ax.bar(
            [i + width/2 for i in x],
            ref_values,
            width,
            label='Reference Kyber512 (ML-KEM)',
            color='#4ECDC4',
            alpha=0.8
        )
        
        # Add value labels on bars
        for bar in bars2:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.4f}',
                ha='center',
                va='bottom',
                fontsize=9
            )
    
    # Add value labels on custom bars
    for bar in bars1:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{height:.4f}',
            ha='center',
            va='bottom',
            fontsize=9
        )
    
    # Formatting
    ax.set_xlabel('Operation', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time (milliseconds)', fontsize=12, fontweight='bold')
    ax.set_title('Kyber Implementation Performance Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(operations)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    plt.close()
    
    return output_path


def generate_report(
    our_timings: Dict[str, float],
    reference_timings: Optional[Dict[str, float]],
    output_dir: str = None
) -> str:
    """
    Generate a JSON report with benchmark results.
    
    Args:
        our_timings: Timings from custom implementation
        reference_timings: Timings from reference implementation (optional)
        output_dir: Directory to save the report
        
    Returns:
        Path to the saved report file
    """
    if output_dir is None:
        output_dir = str(Path(__file__).parent.parent / "report_assets")
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    report_path = Path(output_dir) / "benchmark_results.json"
    
    report = {
        "parameters": {
            "custom_kyber": {
                "n": N,
                "q": Q,
                "k": K,
                "eta1": ETA1,
                "eta2": ETA2,
                "input_bytes": BENCHMARK_MESSAGE_BYTES,
                "note": "Educational scratch implementation with naive polynomial multiplication.",
            },
            "reference_kyber512": {
                "algorithm": "ML-KEM-512",
                "n": 256,
                "q": 3329,
                "k": 2,
                "shared_secret_bytes": 32,
                "note": "pqcrypto reference KEM; internal randomness/noise is not caller-controlled.",
            },
        },
        "custom_kyber": our_timings,
        "reference_kyber512": reference_timings if reference_timings else None,
    }
    
    if reference_timings:
        # Calculate ratios
        ratios = {}
        for op in our_timings.keys():
            ratios[op] = our_timings[op] / reference_timings[op]
        report["performance_ratio"] = ratios
        report["overall_ratio"] = sum(our_timings.values()) / sum(reference_timings.values())
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to: {report_path}")
    return str(report_path)


if __name__ == "__main__":
    from custom_kyber.performance.measure_our_kyber import get_our_kyber_timings
    
    try:
        from reference_kyber.kyber_reference import get_reference_timings
        reference_timings = get_reference_timings(iterations=100)
    except ImportError:
        print("Warning: Could not import reference Kyber")
        reference_timings = None
    
    our_timings = get_our_kyber_timings(iterations=100)
    
    print("\nGenerating visualization...")
    plot_comparison(our_timings, reference_timings)
    
    print("\nGenerating report...")
    generate_report(our_timings, reference_timings)
