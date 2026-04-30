# config.py

Q = 3329        # Kyber/ML-KEM modulus
N = 256         # Kyber/ML-KEM polynomial degree
K = 2           # Kyber512/ML-KEM-512 module rank

ETA1 = 3        # Kyber512 secret/noise parameter
ETA2 = 2        # Kyber512 encryption error parameter

NOISE_MIN = -ETA2
NOISE_MAX = ETA2
BENCHMARK_MESSAGE_BYTES = 32
