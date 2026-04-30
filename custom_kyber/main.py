# main.py

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from custom_kyber.kyber import keygen, encrypt, decrypt
from custom_kyber.utils import message_to_poly, poly_to_message

def main():
    public_key, secret_key = keygen()

    message = "HELLO"
    message_poly = message_to_poly(message)

    ciphertext = encrypt(public_key, message_poly)

    decrypted_poly = decrypt(secret_key, ciphertext)
    decrypted_message = poly_to_message(decrypted_poly)

    print("Original Message:", message)
    print("Decrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()
