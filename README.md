# Custom Kyber

This repository contains a small educational Kyber-style implementation in `custom_kyber/` and a reference ML-KEM-512 wrapper in `reference_kyber/`.

## Layout

```text
custom_kyber/
  __init__.py
  config.py
  kyber.py
  main.py
  utils.py
  verify_setup.py
  performance/
    __init__.py
    compare.py
    measure_our_kyber.py
    visualize.py
main.py
verify_setup.py
reference_kyber/
  __init__.py
  kyber_reference.py
benchmark_runner.py
requirements.txt
report_assets/
```

## Run It

Run the demo from the repository root:

```bash
python main.py
```

Run the benchmark suite:

```bash
python benchmark_runner.py
```

Run the setup check:

```bash
python verify_setup.py
```

## Notes

- The custom implementation uses simplified polynomial arithmetic for learning and benchmarking.
- `reference_kyber/kyber_reference.py` wraps `pqcrypto` when it is installed.
- The repository now keeps a single top-level README; the long-form implementation note file is intentionally left out of the active docs.
