#!/usr/bin/env python3
"""
Main benchmark runner script.

This script runs the complete benchmarking pipeline:
1. Measure custom Kyber implementation
2. Measure reference Kyber512 implementation
3. Generate comparison report
4. Create visualization charts

Usage:
    python benchmark_runner.py [--iterations N] [--output-dir PATH]

Options:
    --iterations N      Number of iterations per operation (default: 100)
    --output-dir PATH   Directory for output files (default: report_assets)
"""

import sys
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from custom_kyber.performance.measure_our_kyber import get_our_kyber_timings
from custom_kyber.performance.compare import compare_implementations, print_summary
from custom_kyber.performance.visualize import plot_comparison, generate_report


def main():
    """Main benchmark runner."""
    parser = argparse.ArgumentParser(
        description='Benchmark custom Kyber vs reference Kyber512'
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=100,
        help='Number of iterations per operation (default: 100)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory for results (default: report_assets)'
    )
    parser.add_argument(
        '--no-visualization',
        action='store_true',
        help='Skip chart generation'
    )
    
    args = parser.parse_args()
    
    if args.output_dir is None:
        args.output_dir = str(Path(__file__).parent / "report_assets")
    
    # Ensure output directory exists
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    print()
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 70 + "║")
    print("║" + "Kyber Implementation Benchmarking Suite".center(70) + "║")
    print("║" + " " * 70 + "║")
    print("╚" + "═" * 70 + "╝")
    print()
    
    try:
        # Run benchmarks
        our_timings, reference_timings = compare_implementations(args.iterations)
        
        # Print summary
        print_summary(our_timings, reference_timings)
        
        # Generate report
        report_path = generate_report(our_timings, reference_timings, args.output_dir)
        print(f"✓ Report generated: {report_path}")
        
        # Generate visualization
        if not args.no_visualization:
            try:
                chart_path = plot_comparison(
                    our_timings,
                    reference_timings,
                    str(Path(args.output_dir) / "performance.png")
                )
                print(f"✓ Visualization generated: {chart_path}")
            except ImportError as e:
                print(f"⚠ Visualization skipped: {e}")
                print("  Install matplotlib with: pip install matplotlib")
        
        print()
        print("✓ Benchmarking complete!")
        print(f"  Results saved to: {args.output_dir}")
        print()
        
        return 0
        
    except Exception as e:
        print(f"✗ Error during benchmarking: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
