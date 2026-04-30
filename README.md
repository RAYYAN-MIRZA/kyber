# ML-KEM Kyber Simplified Implementation and Benchmark Comparison

A simplified educational implementation of the **ML-KEM Kyber** post-quantum cryptographic key encapsulation mechanism. This project demonstrates the core concepts of Kyber cryptography with simplified polynomial operations and small parameters for learning and benchmarking purposes.

It also includes a benchmark suite that compares the custom Python Kyber implementation against a reference **ML-KEM-512** implementation from `pqcrypto`, so you can see the performance gap directly.

## About ML-KEM Kyber

**Kyber** is a lattice-based key encapsulation mechanism (KEM) standardized as **ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism) by NIST. It is designed to resist attacks from quantum computers, making it an important part of post-quantum cryptography.

### Key Features of Kyber

- **Lattice-based security**: Based on the Module Learning With Errors (M-LWE) problem
- **Post-quantum resistant**: Secure against known quantum algorithms
- **Efficient**: Fast key generation, encapsulation, and decapsulation
- **Standardized**: Approved by NIST as part of Post-Quantum Cryptography (PQC)

## Project Structure

```text
kyber/
├── main.py                  # Root entrypoint for the demo
├── verify_setup.py          # Root setup/verification script
├── benchmark_runner.py      # Benchmark pipeline entrypoint
├── custom_kyber/
│   ├── __init__.py
│   ├── config.py           # Configuration parameters
│   ├── kyber.py            # Core Kyber-style functions
│   ├── main.py             # Demo logic
│   ├── utils.py            # Polynomial and message helpers
│   └── performance/
│       ├── __init__.py
│       ├── compare.py
│       ├── measure_our_kyber.py
│       └── visualize.py
├── reference_kyber/
│   ├── __init__.py
│   └── kyber_reference.py  # pqcrypto-backed ML-KEM-512 reference
├── report_assets/
└── requirements.txt
```

## Files Overview

### `custom_kyber/config.py`
Contains configuration parameters used by the custom implementation:
- `Q = 3329`: Modulus used for polynomial coefficients
- `N = 256`: Polynomial degree
- `K = 2`: Module rank for the Kyber512-style structure
- `ETA1` and `ETA2`: Noise parameters for sampling secrets and errors
- `BENCHMARK_MESSAGE_BYTES`: Input size used in the benchmark suite

### `custom_kyber/kyber.py`
Implements the three core functions:
- **`keygen()`**: Generates a public/secret key pair
  - Samples random polynomial matrix `A`
  - Samples secret and error vectors `s` and `e`
  - Computes public key output `t = A*s + e`

- **`encrypt(public_key, message_poly)`**: Encrypts a message polynomial
  - Uses the public key and a message polynomial
  - Returns ciphertext components `(u, v)`

- **`decrypt(secret_key, ciphertext)`**: Decrypts a ciphertext
  - Uses the secret key and ciphertext components
  - Returns a recovered message polynomial

### `custom_kyber/utils.py`
Utility functions for polynomial operations and message conversion:
- `poly_add()`: Addition of two polynomials
- `poly_sub()`: Subtraction of two polynomials
- `poly_mul()`: Negacyclic multiplication modulo `x^N + 1`
- `random_poly()`: Generate a random polynomial with coefficients in `[0, Q)`
- `noise_poly()`: Generate a noise polynomial with small coefficients
- `message_to_poly()`: Convert a string or byte message to a polynomial
- `poly_to_message()`: Convert a polynomial back to a string message

### `custom_kyber/main.py`
Demonstrates the complete workflow:
1. Generate a key pair
2. Convert a message to a polynomial
3. Encrypt the message with the public key
4. Decrypt with the secret key
5. Print the original and decrypted messages

### `custom_kyber/performance/`
Benchmarking and visualization helpers:
- `measure_our_kyber.py`: Measures the custom implementation
- `compare.py`: Compares the custom implementation with the reference KEM
- `visualize.py`: Generates charts and JSON reports

### `reference_kyber/kyber_reference.py`
Provides a reference wrapper around `pqcrypto` for ML-KEM-512 comparison during benchmarking.

## How to Run

### Prerequisites

- Python 3.7 or higher
- `pqcrypto` is optional for the reference benchmark
- `matplotlib` is optional for chart generation

### Run the Demo

From the repository root:

```bash
python main.py
```

Expected output:

```text
Original Message: HELLO
Decrypted Message: HELLO
```

### Run the Setup Check

```bash
python verify_setup.py
```

### Run the Benchmark Suite

```bash
python benchmark_runner.py
```

This benchmark compares:

- the custom Kyber implementation in `custom_kyber/`
- the Python reference ML-KEM-512 wrapper in `reference_kyber/`

You can also skip visualization if you only want timing output:

```bash
python benchmark_runner.py --no-visualization
```

## Modifying the Simulation

You can edit `custom_kyber/main.py` to test different messages:

```python
message = "YOUR_MESSAGE_HERE"
```

You can also adjust the parameters in `custom_kyber/config.py`:

```python
N = 16              # Increase polynomial degree
Q = 7681            # Change modulus
ETA1 = 2            # Reduce secret noise
ETA2 = 1            # Reduce encryption noise
```

## Simplified Implementation Notes

This implementation is a simplified educational version and differs from the full ML-KEM standard:

1. **Educational arithmetic**: The custom implementation is designed to be easy to inspect and benchmark
2. **Smaller scope than production KEMs**: It keeps the polynomial and module structure approachable
3. **No production serialization**: It does not implement full byte-level encodings used in deployed libraries
4. **No CPA-to-CCA conversion**: The custom flow is intentionally simplified for learning
5. **Simplified message handling**: Message conversion is basic and intended for demonstration

## Mathematical Concepts

### Key Generation

```text
A <- R(Q)                    # Random polynomial matrix
s <- eta1                    # Secret polynomial vector
e <- eta1                    # Error polynomial vector
t := A*s + e                 # Public key component
```

### Encryption

```text
r <- eta1                    # Random vector
e1 <- eta2                   # Error vector
e2 <- eta2                   # Error polynomial
u := A^T*r + e1              # Ciphertext component 1
v := t*r + e2 + m            # Ciphertext component 2
```

### Decryption

```text
m := v - u*s                 # Recover message
```

## Learning Resources

- [NIST ML-KEM Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [Kyber Official Specification](https://pq-crystals.org/kyber/)
- [Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography/)

## Disclaimer

This is an educational implementation for learning purposes only. It is not suitable for production use due to:

- Simplified design choices
- Lack of production hardening
- No full CCA security conversion
- Educational-quality polynomial operations

For real-world applications, use well-tested, audited implementations like [liboqs](https://github.com/open-quantum-safe/liboqs) or other NIST-approved libraries.

## Author Notes

This project demonstrates the core mathematical operations and flow of ML-KEM Kyber in a simplified, easy-to-understand manner. It is intended for students and learners exploring post-quantum cryptography.
