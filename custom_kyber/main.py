# main.py — ML-KEM-512 demo: encapsulate a shared secret, decapsulate, optional XOR demo.

import hashlib
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from custom_kyber.kyber import decapsulate, encapsulate, generate_keypair


def main() -> None:
    public_key, secret_key = generate_keypair()
    ciphertext, shared_secret_encap = encapsulate(public_key)
    shared_secret_decap = decapsulate(secret_key, ciphertext)

    assert shared_secret_encap == shared_secret_decap

    print("ML-KEM-512 (Kyber512) KEM demo")
    print(f"  Public key:  {len(public_key)} bytes")
    print(f"  Secret key:  {len(secret_key)} bytes")
    print(f"  Ciphertext:  {len(ciphertext)} bytes")
    print(f"  Shared key:  {len(shared_secret_encap)} bytes (use with AES-GCM or similar after a KDF)")
    print(f"  Match:       {shared_secret_encap.hex()[:32]}… == {shared_secret_decap.hex()[:32]}…")

    # Pedagogical “hybrid” step without extra deps: derive 32-byte stream key via SHA-256.
    demo_msg = b"hello supervisor"
    k = hashlib.sha256(shared_secret_encap + b"demo").digest()
    enc = bytes(m ^ k[i % len(k)] for i, m in enumerate(demo_msg))
    dec = bytes(c ^ k[i % len(k)] for i, c in enumerate(enc))
    print(f"  Demo XOR:    {dec!r}")


if __name__ == "__main__":
    main()
