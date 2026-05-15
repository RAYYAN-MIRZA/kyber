# ML-KEM-512 Kyber Implementation and Benchmark Suite

A from-scratch educational Python implementation of **ML-KEM-512**, the Kyber512 parameter set standardized by NIST as **ML-KEM** in FIPS 203.

The current custom implementation is a byte-level key encapsulation mechanism (KEM): it generates an ML-KEM-512 keypair, encapsulates a 32-byte shared secret to a public key, and decapsulates that shared secret with the secret key. The demo then derives an AES-256 key from that shared secret and uses AES-GCM to encrypt the actual message. The project also includes benchmark tooling that compares the custom Python implementation against the `pqcrypto` ML-KEM-512 implementation.

> Educational note: this repository is for learning, inspection, and benchmarking. Do not use it for production cryptography.

## What This Implements

The custom implementation now exposes the standard KEM workflow:

- `generate_keypair()` -> `(public_key, secret_key)`
- `encapsulate(public_key)` -> `(ciphertext, shared_secret)`
- `decapsulate(secret_key, ciphertext)` -> `shared_secret`

The public wrapper is `custom_kyber/kyber.py`, while the implementation lives under `custom_kyber/ml_kem512/`.

Implemented ML-KEM-512 sizes:

| Item | Size |
| --- | ---: |
| Public key | 800 bytes |
| Secret key | 1632 bytes |
| Ciphertext | 768 bytes |
| Shared secret | 32 bytes |

Core parameters:

| Parameter | Value |
| --- | ---: |
| `N` | 256 |
| `Q` | 3329 |
| `K` | 2 |
| `ETA1` | 3 |
| `ETA2` | 2 |

## Project Structure

```text
kyber/
|-- main.py                         # Root entrypoint for the custom KEM demo
|-- verify_setup.py                 # Setup, import, and round-trip verification
|-- benchmark_runner.py             # Benchmark pipeline entrypoint
|-- requirements.txt
|-- custom_kyber/
|   |-- __init__.py
|   |-- config.py                   # Shared parameters and byte-size constants
|   |-- kyber.py                    # Public custom ML-KEM-512 wrapper API
|   |-- main.py                     # Demo: keygen, encapsulate, decapsulate
|   |-- utils.py                    # Legacy/simple polynomial helpers
|   |-- verify_setup.py             # Compatibility wrapper for root verifier
|   |-- ml_kem512/
|   |   |-- __init__.py             # Exports the ML-KEM-512 public API
|   |   |-- params.py               # ML-KEM-512 constants and byte sizes
|   |   |-- kem.py                  # CCA KEM: keypair, encaps, decaps
|   |   |-- indcpa.py               # CPA encryption core
|   |   |-- polynomial.py           # Polynomial/polyvec encode, compress, arithmetic
|   |   |-- ntt.py                  # Number theoretic transform operations
|   |   |-- cbd.py                  # Centered binomial noise sampling
|   |   |-- reduce_ops.py           # Montgomery/Barrett reduction helpers
|   |   `-- symmetric.py            # SHA3/SHAKE-based hash and XOF helpers
|   `-- performance/
|       |-- __init__.py
|       |-- measure_our_kyber.py    # Custom implementation timings
|       |-- compare.py              # Custom vs reference benchmark comparison
|       `-- visualize.py            # JSON report and chart generation
|-- reference_kyber/
|   |-- __init__.py
|   `-- kyber_reference.py          # pqcrypto-backed ML-KEM-512 reference wrapper
`-- report_assets/                  # Generated benchmark reports/charts
```

## Implementation Overview

### `custom_kyber/kyber.py`

This is the public import surface for the custom implementation. It re-exports the ML-KEM-512 API from `custom_kyber.ml_kem512`:

- `generate_keypair()`
- `keypair_derand(coins)`
- `encapsulate(public_key)`
- `encapsulate_derand(public_key, coins)`
- `decapsulate(secret_key, ciphertext)`
- `PUBLICKEYBYTES`, `SECRETKEYBYTES`, `CIPHERTEXTBYTES`, `SSBYTES`

### `custom_kyber/ml_kem512/kem.py`

Implements the CCA-secure KEM layer:

1. Generate or accept random coins.
2. Build the IND-CPA keypair.
3. Store the IND-CPA secret key, public key, hash of the public key, and fallback secret in the ML-KEM secret key.
4. Encapsulate by deriving coins and a shared secret with SHA3/SHAKE helpers.
5. Decapsulate by decrypting, re-encrypting for verification, and selecting the correct or fallback shared secret.

### `custom_kyber/ml_kem512/indcpa.py`

Implements the CPA public-key encryption core used inside ML-KEM:

- deterministic IND-CPA keypair generation
- matrix generation with SHAKE128 rejection sampling
- IND-CPA encryption of a 32-byte message
- IND-CPA decryption back to a 32-byte message

### `custom_kyber/ml_kem512/polynomial.py`

Contains polynomial and vector operations used by the KEM:

- byte encoding/decoding
- compression/decompression
- message-to-polynomial and polynomial-to-message conversion
- NTT and inverse NTT wrappers
- polynomial/vector addition, subtraction, reduction, and base multiplication

### Other ML-KEM Modules

- `params.py`: ML-KEM-512 constants and serialized byte lengths.
- `ntt.py`: NTT, inverse NTT, and base multiplication primitives.
- `cbd.py`: centered binomial distribution samplers for `ETA1` and `ETA2`.
- `reduce_ops.py`: finite-field reduction helpers.
- `symmetric.py`: SHA3-256, SHA3-512, SHAKE128, SHAKE256, and PRF/KDF helpers.

## How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

`matplotlib` is used for benchmark charts. `pqcrypto` is used only for the optional reference comparison.

### Run the Demo

From the repository root:

```bash
python main.py
```

Expected output shape:

```text
ML-KEM-512 (Kyber512) + AES-GCM demo
  Flow:        ML-KEM -> HKDF-SHA256 -> AES-256-GCM
  Public key:  800 bytes
  Secret key:  1632 bytes
  KEM ct:      768 bytes
  ML-KEM ss:   32 bytes
  AES key:     32 bytes
  AES nonce:   12 bytes
  AES ct+tag:  ...
  Secret ok:   ... == ...
  Message:     ML-KEM establishes the key; AES-GCM encrypts the real message.
  NTT/Mont:    polynomial multiplication uses NTT butterflies and Montgomery reduction
```

This is a KEM-DEM style workflow:

1. ML-KEM establishes the shared secret.
2. HKDF-SHA256 derives a symmetric AES-256 key from that secret.
3. AES-GCM encrypts and authenticates the actual message.

ML-KEM does not replace AES. It replaces classical key-establishment mechanisms such as RSA key exchange or Diffie-Hellman. AES remains the efficient symmetric encryption layer.

### Run Setup Verification

```bash
python verify_setup.py
```

This checks the expected file structure, optional dependencies, imports, and a KEM round trip.

### Run Benchmarks

```bash
python benchmark_runner.py
```

Useful options:

```bash
python benchmark_runner.py --iterations 25
python benchmark_runner.py --no-visualization
python benchmark_runner.py --output-dir report_assets
```

The benchmark measures:

- KeyGen: `generate_keypair()`
- Encrypt: KEM encapsulation via `encapsulate(public_key)`
- Decrypt: KEM decapsulation via `decapsulate(secret_key, ciphertext)`

If `pqcrypto` is installed, the benchmark also compares against `pqcrypto.kem.ml_kem_512`. If it is unavailable, the custom implementation is still benchmarked and the reference comparison is skipped.

## Programmatic Usage

```python
from custom_kyber.kyber import decapsulate, encapsulate, generate_keypair
from custom_kyber.main import derive_aes_key

public_key, secret_key = generate_keypair()
ciphertext, shared_secret_sender = encapsulate(public_key)
shared_secret_receiver = decapsulate(secret_key, ciphertext)

assert shared_secret_sender == shared_secret_receiver

aes_key_sender = derive_aes_key(shared_secret_sender)
aes_key_receiver = derive_aes_key(shared_secret_receiver)
assert aes_key_sender == aes_key_receiver
```

## Supervisor Explanation

The project follows the real ML-KEM plus AES architecture:

```text
Bob:   ML-KEM KeyGen        -> public key pk, secret key sk
Alice: ML-KEM Encaps(pk)    -> KEM ciphertext ct, shared secret K
Bob:   ML-KEM Decaps(sk,ct) -> same shared secret K
Both:  HKDF-SHA256(K)       -> AES-256 key
Alice: AES-GCM encrypts the actual message
Bob:   AES-GCM decrypts the actual message
```

Inside ML-KEM, the expensive polynomial arithmetic is accelerated with NTT. The NTT implementation uses butterfly operations, and modular multiplication uses Montgomery reduction. In this project those pieces live in:

- `custom_kyber/ml_kem512/ntt.py`
- `custom_kyber/ml_kem512/reduce_ops.py`
- `custom_kyber/ml_kem512/polynomial.py`

For deterministic tests, use the `_derand` helpers:

```python
from custom_kyber.kyber import encapsulate_derand, keypair_derand

public_key, secret_key = keypair_derand(b"\x00" * 64)
ciphertext, shared_secret = encapsulate_derand(public_key, b"\x01" * 32)
```

## Notes on the Older Toy Helpers

`custom_kyber/utils.py` still contains simple polynomial helper functions from the earlier educational version. The active ML-KEM-512 flow does not use the old string-message encrypt/decrypt demo. The current demo and benchmarks operate on the KEM API and fixed-size byte strings.

## Benchmark Reports

Generated benchmark assets are written to `report_assets/` by default:

- `benchmark_results.json`
- `performance.png` when visualization is enabled

These files are generated outputs and can be refreshed by re-running `benchmark_runner.py`.

## Learning Resources

- [NIST FIPS 203: ML-KEM Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [CRYSTALS-Kyber](https://pq-crystals.org/kyber/)
- [NIST Post-Quantum Cryptography Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Open Quantum Safe liboqs](https://github.com/open-quantum-safe/liboqs)

## Disclaimer

This project is an educational implementation. It is not audited, hardened, or intended for real-world cryptographic deployment. For production systems, use a maintained, audited implementation from a trusted cryptographic library.
