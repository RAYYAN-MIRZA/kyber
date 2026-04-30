# kyber.py

from custom_kyber.config import K, ETA1, ETA2
from custom_kyber.utils import poly_add, poly_mul, poly_sub, random_poly, noise_poly


def poly_sum(products):
    total = [0] * len(products[0])
    for poly in products:
        total = poly_add(total, poly)
    return total

def keygen():
    # Public matrix A, shaped like Kyber512's k x k polynomial matrix.
    A = [[random_poly() for _ in range(K)] for _ in range(K)]

    # Secret and error vectors use Kyber512's eta1-sized noise.
    s = [noise_poly(ETA1) for _ in range(K)]
    e = [noise_poly(ETA1) for _ in range(K)]

    # Public key: t = A*s + e
    t = []
    for i in range(K):
        products = [poly_mul(A[i][j], s[j]) for j in range(K)]
        t.append(poly_add(poly_sum(products), e[i]))

    public_key = (A, t)
    secret_key = s

    return public_key, secret_key



def encrypt(public_key, message_poly):
    A, t = public_key

    # Random and error vectors use Kyber512-sized parameters.
    r = [noise_poly(ETA1) for _ in range(K)]
    e1 = [noise_poly(ETA2) for _ in range(K)]
    e2 = noise_poly(ETA2)

    # u = A^T*r + e1
    u = []
    for i in range(K):
        products = [poly_mul(A[j][i], r[j]) for j in range(K)]
        u.append(poly_add(poly_sum(products), e1[i]))

    # v = t*r + e2 + m
    temp = poly_add(poly_sum([poly_mul(t[j], r[j]) for j in range(K)]), e2)
    v = poly_add(temp, message_poly)

    ciphertext = (u, v)

    return ciphertext
def decrypt(secret_key, ciphertext):
    u, v = ciphertext
    s = secret_key

    # Compute u * s
    us = poly_sum([poly_mul(u[j], s[j]) for j in range(K)])

    # Recover message: m = v - (u * s)
    m = poly_sub(v, us)

    return m
