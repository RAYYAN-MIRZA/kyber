# kyber.py

from utils import poly_add, poly_mul, random_poly, noise_poly

def keygen():
    # Public matrix A (simplified as single poly)
    A = random_poly()

    # Secret key s
    s = noise_poly()

    # Error e
    e = noise_poly()

    # Public key: t = A*s + e
    t = poly_add(poly_mul(A, s), e)

    public_key = (A, t)
    secret_key = s

    return public_key, secret_key



from utils import poly_add, poly_mul, noise_poly

def encrypt(public_key, message_poly):
    A, t = public_key

    # random vector
    r = noise_poly()

    # errors
    e1 = noise_poly()
    e2 = noise_poly()

    # u = A*r + e1
    u = poly_add(poly_mul(A, r), e1)

    # v = t*r + e2 + m
    temp = poly_add(poly_mul(t, r), e2)
    v = poly_add(temp, message_poly)

    ciphertext = (u, v)

    return ciphertext


from utils import poly_sub, poly_mul

def decrypt(secret_key, ciphertext):
    u, v = ciphertext
    s = secret_key

    # Compute u * s
    us = poly_mul(u, s)

    # Recover message: m = v - (u * s)
    m = poly_sub(v, us)

    return m