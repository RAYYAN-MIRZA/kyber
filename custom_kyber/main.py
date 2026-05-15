# main.py -- ML-KEM-512 + AES-GCM demo.

import sys
from os import urandom
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.hashes import SHA256
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "This demo needs the 'cryptography' package for AES-GCM.\n"
        "Install dependencies with: pip install -r requirements.txt"
    ) from exc

from custom_kyber.kyber import decapsulate, encapsulate, generate_keypair


def derive_aes_key(shared_secret: bytes) -> bytes:
    """Derive a 256-bit AES key from the ML-KEM shared secret."""
    return HKDF(
        algorithm=SHA256(),
        length=32,
        salt=None,
        info=b"ML-KEM-512 demo AES-GCM key",
    ).derive(shared_secret)


def main() -> None:
    message = b"ML-KEM establishes the key; AES-GCM encrypts the real message."

    # Step 1: Bob generates ML-KEM public/private keys.
    public_key, secret_key = generate_keypair()

    # Step 2: Alice encapsulates to Bob's public key.
    ciphertext, shared_secret_encap = encapsulate(public_key)

    # Step 3: Bob decapsulates the ML-KEM ciphertext.
    shared_secret_decap = decapsulate(secret_key, ciphertext)
    assert shared_secret_encap == shared_secret_decap

    # Step 4: Both sides derive the same AES-256 key from the ML-KEM secret.
    aes_key_sender = derive_aes_key(shared_secret_encap)
    aes_key_receiver = derive_aes_key(shared_secret_decap)
    assert aes_key_sender == aes_key_receiver

    # Step 5: AES-GCM encrypts/decrypts the actual message.
    nonce = urandom(12)
    aes_sender = AESGCM(aes_key_sender)
    aes_receiver = AESGCM(aes_key_receiver)
    aes_ciphertext = aes_sender.encrypt(nonce, message, associated_data=ciphertext)
    plaintext = aes_receiver.decrypt(nonce, aes_ciphertext, associated_data=ciphertext)
    assert plaintext == message

    print("ML-KEM-512 (Kyber512) + AES-GCM demo")
    print("  Flow:        ML-KEM -> HKDF-SHA256 -> AES-256-GCM")
    print(f"  Public key:  {len(public_key)} bytes")
    print(f"  Secret key:  {len(secret_key)} bytes")
    print(f"  KEM ct:      {len(ciphertext)} bytes")
    print(f"  ML-KEM ss:   {len(shared_secret_encap)} bytes")
    print(f"  AES key:     {len(aes_key_sender)} bytes")
    print(f"  AES nonce:   {len(nonce)} bytes")
    print(f"  AES ct+tag:  {len(aes_ciphertext)} bytes")
    print(f"  Secret ok:   {shared_secret_encap.hex()[:32]}... == {shared_secret_decap.hex()[:32]}...")
    print(f"  Message:     {plaintext.decode('utf-8')}")
    print("  NTT/Mont:    polynomial multiplication uses NTT butterflies and Montgomery reduction")


if __name__ == "__main__":
    main()
