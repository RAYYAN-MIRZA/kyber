# utils.py

import random

from custom_kyber.config import Q, N, ETA2

def mod_q(x):
    return x % Q

def poly_add(a, b):
    return [(a[i] + b[i]) % Q for i in range(N)]

def poly_sub(a, b):
    return [(a[i] - b[i]) % Q for i in range(N)]

def poly_mul(a, b):
    # Negacyclic multiplication modulo x^N + 1, matching Kyber's ring shape.
    result = [0] * N
    for i in range(N):
        for j in range(N):
            degree = i + j
            if degree >= N:
                result[degree - N] -= a[i] * b[j]
            else:
                result[degree] += a[i] * b[j]
    return [x % Q for x in result]

def random_poly():
    return [random.randint(0, Q-1) for _ in range(N)]

def noise_poly(eta=ETA2):
    return [random.randint(-eta, eta) for _ in range(N)]



def message_to_poly(message):
    if isinstance(message, str):
        data = message.encode("utf-8")
    else:
        data = bytes(message)

    data = data[: N // 8].ljust(N // 8, b"\x00")
    poly = []

    for byte in data:
        for bit_index in range(8):
            bit = (byte >> bit_index) & 1
            poly.append(Q // 2 if bit else 0)

    return poly[:N]



def poly_to_message(poly):
    output = bytearray()

    for offset in range(0, N, 8):
        byte = 0
        for bit_index, value in enumerate(poly[offset:offset + 8]):
            centered = value % Q
            bit = 1 if Q // 4 <= centered <= 3 * Q // 4 else 0
            byte |= bit << bit_index
        output.append(byte)

    return bytes(output).rstrip(b"\x00").decode("utf-8", errors="ignore")
