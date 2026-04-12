# utils.py

import random
from config import Q, N, NOISE_MIN, NOISE_MAX

def mod_q(x):
    return x % Q

def poly_add(a, b):
    return [(a[i] + b[i]) % Q for i in range(N)]

def poly_sub(a, b):
    return [(a[i] - b[i]) % Q for i in range(N)]

def poly_mul(a, b):
    # simple polynomial multiplication (no NTT)
    result = [0] * N
    for i in range(N):
        for j in range(N):
            result[(i + j) % N] += a[i] * b[j]
    return [x % Q for x in result]

def random_poly():
    return [random.randint(0, Q-1) for _ in range(N)]

def noise_poly():
    return [random.randint(NOISE_MIN, NOISE_MAX) for _ in range(N)]



def message_to_poly(message):
    # simple: convert chars to ASCII mod Q
    poly = [ord(c) % Q for c in message]
    
    # pad to length N
    while len(poly) < N:
        poly.append(0)
    
    return poly[:N]    



def poly_to_message(poly):
    message = ""
    for val in poly:
        if val != 0:
            message += chr(val % 128)  # basic ASCII
    return message