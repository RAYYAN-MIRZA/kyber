#!/usr/bin/env python3
"""
Verification and setup script for the benchmarking suite.

This script checks if all dependencies are installed and the structure is correct.
"""

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def check_structure():
    """Check if folder structure is correct."""
    print("📁 Checking folder structure...")

    required_files = [
        "main.py",
        "verify_setup.py",
        "benchmark_runner.py",
        "custom_kyber/__init__.py",
        "custom_kyber/main.py",
        "custom_kyber/kyber.py",
        "custom_kyber/utils.py",
        "custom_kyber/config.py",
        "custom_kyber/performance/__init__.py",
        "custom_kyber/performance/measure_our_kyber.py",
        "custom_kyber/performance/compare.py",
        "custom_kyber/performance/visualize.py",
        "reference_kyber/__init__.py",
        "reference_kyber/kyber_reference.py",
    ]

    project_root = Path(__file__).resolve().parent
    missing = []

    for file_path in required_files:
        full_path = project_root / file_path
        if not full_path.exists():
            missing.append(file_path)

    if missing:
        print("  ✗ Missing files:")
        for f in missing:
            print(f"    - {f}")
        return False

    print("  ✓ All required files present")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")

    dependencies = {
        "matplotlib": "For visualization charts (optional)",
        "pqcrypto": "For reference Kyber512 comparison (optional)",
    }

    missing = []
    optional = []

    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"  ✓ {package:<15} - {description}")
        except Exception as e:
            if package in ["pqcrypto", "matplotlib"]:
                optional.append((package, description))
                error_type = type(e).__name__
                print(f"  ⚠ {package:<15} - {description}")
                if error_type != "ImportError":
                    print(f"      ({error_type}: Import failed, will be skipped)")
            else:
                missing.append((package, description))
                print(f"  ✗ {package:<15} - {description}")

    missing = [item for item in missing if item[0] not in {"pqcrypto", "matplotlib"}]

    return len(missing) == 0, optional


def check_kyber_imports():
    """Check if custom Kyber modules can be imported."""
    print("\n📚 Checking custom Kyber imports...")

    try:
        from custom_kyber.kyber import keygen, encrypt, decrypt
        from custom_kyber.utils import message_to_poly, poly_to_message
        print("  ✓ Custom Kyber modules importable")
        return True
    except ImportError as e:
        print(f"  ✗ Error importing Kyber: {e}")
        return False


def print_setup_instructions(optional):
    """Print setup instructions."""
    if not optional:
        return

    print("\n🔧 OPTIONAL SETUP")
    print("-" * 70)

    if any(pkg == "matplotlib" for pkg, _ in optional):
        print("\nOptional: Install matplotlib for visualization charts")
        print("  pip install matplotlib")

    if any(pkg == "pqcrypto" for pkg, _ in optional):
        print("\nOptional: Install pqcrypto for reference Kyber512 comparison")
        print("  pip install pqcrypto")


def print_next_steps():
    """Print next steps."""
    print("\n✅ READY TO START!")
    print("-" * 70)
    print("\nNext steps:")
    print("  1. Run the complete benchmark:")
    print("     python benchmark_runner.py")
    print("\n  2. Or see quick start guide:")
    print("     python main.py")
    print("\n  3. Or read the project README:")
    print("     - README.md")
    print()


def main():
    """Main verification."""
    print()
    print("╔" + "═" * 70 + "╗")
    print("║" + "Kyber Benchmarking Suite - Setup Verification".center(70) + "║")
    print("╚" + "═" * 70 + "╝")
    print()

    structure_ok = check_structure()
    deps_ok, optional = check_dependencies()
    imports_ok = check_kyber_imports()

    print()
    print("╔" + "═" * 70 + "╗")

    if structure_ok and imports_ok:
        print("║" + "✓ Setup verification PASSED".center(70) + "║")
    else:
        print("║" + "✗ Setup verification FAILED".center(70) + "║")

    if not deps_ok:
        print("║" + "⚠ Some dependencies missing (see above)".center(70) + "║")

    print("╚" + "═" * 70 + "╝")

    print_setup_instructions(optional)

    if structure_ok and imports_ok:
        print_next_steps()
        return 0

    print("\n✗ Please fix the issues above before running benchmarks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
