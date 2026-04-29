# ML-KEM Kyber Simplified Implementation Simulation

A simplified educational implementation of the **ML-KEM Kyber** post-quantum cryptographic key encapsulation mechanism. This project demonstrates the core concepts of Kyber cryptography with simplified polynomial operations and small parameters for learning purposes.

## About ML-KEM Kyber

**Kyber** is a lattice-based key encapsulation mechanism (KEM) standardized as **ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism) by NIST. It's designed to be resistant to attacks from quantum computers, making it a crucial component of post-quantum cryptography.

### Key Features of Kyber:
- **Lattice-based security**: Based on the Module Learning With Errors (M-LWE) problem
- **Post-quantum resistant**: Secure against known quantum algorithms
- **Efficient**: Fast key generation, encryption, and decryption
- **Standardized**: Approved by NIST as part of Post-Quantum Cryptography (PQC)

## Project Structure

```
kyber/
├── main.py          # Entry point - demonstrates keygen, encrypt, decrypt
├── kyber.py         # Core Kyber functions (keygen, encrypt, decrypt)
├── utils.py         # Utility functions (polynomial operations, message conversion)
├── config.py        # Configuration parameters (modulus, polynomial degree, noise range)
└── README.md        # This file
```

## Files Overview

### `config.py`
Contains configuration parameters:
- `Q = 3329`: Modulus (same as Kyber standard, but simplified for small implementation)
- `N = 8`: Polynomial degree (small for simplicity; full Kyber uses N=256)
- `NOISE_MIN/MAX`: Range for noise generation in key generation and encryption

### `kyber.py`
Implements three core functions:
- **`keygen()`**: Generates a public/secret key pair
  - Samples random polynomial A and noise polynomials s, e
  - Public key = (A, t) where t = A*s + e
  - Secret key = s
  
- **`encrypt(public_key, message_poly)`**: Encrypts a message polynomial
  - Takes public key and message polynomial
  - Returns ciphertext (u, v)
  
- **`decrypt(secret_key, ciphertext)`**: Decrypts a ciphertext
  - Takes secret key and ciphertext
  - Returns decrypted message polynomial

### `utils.py`
Utility functions for polynomial operations:
- `poly_add()`: Addition of two polynomials
- `poly_sub()`: Subtraction of two polynomials
- `poly_mul()`: Multiplication of two polynomials (naive method, no NTT)
- `random_poly()`: Generate random polynomial with coefficients in [0, Q)
- `noise_poly()`: Generate noise polynomial with small coefficients
- `message_to_poly()`: Convert string message to polynomial
- `poly_to_message()`: Convert polynomial back to string message

### `main.py`
Demonstration of the complete workflow:
1. Generate key pair
2. Convert message to polynomial
3. Encrypt message with public key
4. Decrypt with secret key
5. Print original and decrypted messages

## How to Run

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Running the Simulation

1. **Navigate to the project directory:**
   ```bash
   cd kyber
   ```

2. **Run the main simulation:**
   ```bash
   python main.py
   ```

3. **Expected Output:**
   ```
   Original Message: HELLO
   Decrypted Message: HELLO
   ```

### Modifying the Simulation

You can modify `main.py` to test with different messages or parameters:

```python
# In main.py, change the message
message = "YOUR_MESSAGE_HERE"
```

Or adjust parameters in `config.py`:

```python
N = 16              # Increase polynomial degree
Q = 7681            # Change modulus
NOISE_MIN = -3
NOISE_MAX = 3       # Increase noise range
```

## Simplified Implementation Notes

This implementation is a **simplified educational version** and differs from the full ML-KEM standard:

1. **No NTT (Number Theoretic Transform)**: Uses naive polynomial multiplication (O(N²) instead of O(N log N))
2. **Small Parameters**: Uses N=8 and Q=3329 vs. N=256 and Q=3329 in standard Kyber
3. **Single Polynomial**: Simplified A matrix to single polynomial vs. 2D matrix in real Kyber
4. **No Compression**: No coefficient encoding/decoding as in real Kyber
5. **No CPA-to-CCA Conversion**: Basic implementation without CCA security conversion
6. **Simplified Message Format**: Basic ASCII conversion vs. binary encoding

## Mathematical Concepts

### Key Generation
```
A ← R(Q)                    # Random polynomial
s ← ηs                      # Noise polynomial
e ← ηe                      # Error polynomial
t := A·s + e                # Public parameter
```

### Encryption
```
r ← ηr                      # Random vector
e1 ← ηe1                    # Error
e2 ← ηe2                    # Error
u := A·r + e1               # Ciphertext component 1
v := t·r + e2 + m           # Ciphertext component 2
```

### Decryption
```
m := v - u·s                # Recover message
```

## Learning Resources

- [NIST ML-KEM Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [Kyber Official Specification](https://pq-crystals.org/kyber/)
- [Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography/)

## Disclaimer

⚠️ **This is an educational implementation for learning purposes only. It is NOT suitable for production use due to:**
- Simplified parameters (small N and Q)
- Lack of proper security measures
- No CCA security conversion
- Educational quality polynomial operations

For real-world applications, use well-tested, audited implementations like [liboqs](https://github.com/open-quantum-safe/liboqs) or other NIST-approved libraries.

## Author Notes

This project demonstrates the core mathematical operations and flow of ML-KEM Kyber in a simplified, easy-to-understand manner. It's ideal for students and learners interested in post-quantum cryptography.
