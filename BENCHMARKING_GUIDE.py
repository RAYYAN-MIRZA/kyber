#!/usr/bin/env python3
"""
Quick start guide for benchmarking setup.

This script provides instructions and quick-start commands.
"""

import sys
from pathlib import Path


def print_banner():
    print()
    print("╔" + "═" * 70 + "╗")
    print("║" + "Kyber Benchmarking Setup - Quick Start Guide".center(70) + "║")
    print("╚" + "═" * 70 + "╝")
    print()


def print_requirements():
    print("📦 REQUIRED PACKAGES")
    print("-" * 70)
    print()
    print("1. matplotlib (for visualization)")
    print("   pip install matplotlib")
    print()
    print("2. pqcrypto (for reference Kyber512)")
    print("   pip install pqcrypto")
    print()


def print_folder_structure():
    print("📁 FOLDER STRUCTURE")
    print("-" * 70)
    print()
    print("kyber/")
    print("├── kyber.py                      # Your Kyber implementation")
    print("├── utils.py                      # Utility functions")
    print("├── main.py                       # Original main example")
    print("├── config.py                     # Configuration")
    print("│")
    print("├── benchmark_runner.py           # Main benchmark orchestrator")
    print("│")
    print("├── performance/                  # Performance measurement module")
    print("│   ├── __init__.py")
    print("│   ├── measure_our_kyber.py      # Measure your implementation")
    print("│   ├── compare.py                # Compare both implementations")
    print("│   └── visualize.py              # Generate charts and reports")
    print("│")
    print("├── reference_kyber/              # Reference implementation")
    print("│   ├── __init__.py")
    print("│   └── kyber_reference.py        # Standard Kyber512 (pqcrypto)")
    print("│")
    print("└── report_assets/                # Output directory")
    print("    ├── performance.png           # Generated comparison chart")
    print("    └── benchmark_results.json    # Detailed results")
    print()


def print_usage():
    print("🚀 USAGE")
    print("-" * 70)
    print()
    print("1. BASIC USAGE (with defaults):")
    print("   python benchmark_runner.py")
    print()
    print("2. WITH CUSTOM ITERATIONS (e.g., 200):")
    print("   python benchmark_runner.py --iterations 200")
    print()
    print("3. CUSTOM OUTPUT DIRECTORY:")
    print("   python benchmark_runner.py --output-dir ./my_results")
    print()
    print("4. SKIP VISUALIZATION:")
    print("   python benchmark_runner.py --no-visualization")
    print()
    print("5. RUN INDIVIDUAL MODULES:")
    print()
    print("   a) Just measure your implementation:")
    print("      python -m performance.measure_our_kyber")
    print()
    print("   b) Just run comparison (if pqcrypto available):")
    print("      python -m performance.compare")
    print()
    print("   c) Just visualize (requires previous benchmark data):")
    print("      python -m performance.visualize")
    print()


def print_output_files():
    print("📊 OUTPUT FILES")
    print("-" * 70)
    print()
    print("report_assets/")
    print("├── performance.png               # Bar chart comparison")
    print("├── benchmark_results.json        # Detailed timing data")
    print("└── ...")
    print()
    print("performance.png contains:")
    print("  - Bar chart comparing custom vs reference Kyber")
    print("  - Three operations: KeyGen, Encrypt, Decrypt")
    print("  - Actual timing values labeled on bars")
    print()
    print("benchmark_results.json contains:")
    print("  - Timing for custom implementation")
    print("  - Timing for reference Kyber512 (if available)")
    print("  - Performance ratios")
    print()


def print_key_modules():
    print("🔧 KEY MODULES")
    print("-" * 70)
    print()
    
    print("measure_our_kyber.py")
    print("  └─ get_our_kyber_timings(iterations)")
    print("     └─ Returns: Dict[str, float]  {KeyGen, Encrypt, Decrypt} in ms")
    print()
    
    print("kyber_reference.py")
    print("  └─ get_reference_timings(iterations)")
    print("     └─ Returns: Dict[str, float]  {KeyGen, Encrypt, Decrypt} in ms")
    print()
    
    print("visualize.py")
    print("  ├─ plot_comparison(our, reference, output_path)")
    print("  │  └─ Generates: Bar chart PNG")
    print("  └─ generate_report(our, reference, output_dir)")
    print("     └─ Generates: JSON report with detailed metrics")
    print()


def print_example_workflow():
    print("💡 EXAMPLE WORKFLOW")
    print("-" * 70)
    print()
    print("Step 1: Install dependencies")
    print("  pip install matplotlib pqcrypto")
    print()
    print("Step 2: Run benchmark with 150 iterations")
    print("  python benchmark_runner.py --iterations 150")
    print()
    print("Step 3: Check results")
    print("  - Open report_assets/performance.png in an image viewer")
    print("  - Read report_assets/benchmark_results.json for detailed data")
    print()
    print("Step 4: Use in your report")
    print("  - Include performance.png in your technical report")
    print("  - Reference the timing data from benchmark_results.json")
    print()


def print_advanced_options():
    print("⚙️  ADVANCED OPTIONS")
    print("-" * 70)
    print()
    
    print("CUSTOM BENCHMARKING IN PYTHON:")
    print()
    print("  from performance import get_our_kyber_timings, plot_comparison")
    print("  from reference_kyber import get_reference_timings")
    print()
    print("  our = get_our_kyber_timings(iterations=500)")
    print("  ref = get_reference_timings(iterations=500)")
    print("  plot_comparison(our, ref, 'custom_output.png')")
    print()


def print_notes():
    print("📝 IMPORTANT NOTES")
    print("-" * 70)
    print()
    print("1. The benchmark measures end-to-end operation time")
    print("   (includes overhead, not just pure cryptographic operations)")
    print()
    print("2. Results may vary between runs due to system load")
    print("   Use multiple iterations for more stable average times")
    print()
    print("3. Custom Kyber is expected to be slower than reference because:")
    print("   - Simplified parameters (N=8 vs N=256)")
    print("   - Naive polynomial multiplication (O(N²) vs O(N log N) with NTT)")
    print("   - No optimizations or assembly code")
    print()
    print("4. pqcrypto is optional for:")
    print("   - Reference Kyber512 comparison")
    print("   - On Windows: Use pre-built wheels or install via conda")
    print()


def main():
    print_banner()
    print_requirements()
    print_folder_structure()
    print_usage()
    print_output_files()
    print_key_modules()
    print_example_workflow()
    print_advanced_options()
    print_notes()
    print()


if __name__ == "__main__":
    main()
