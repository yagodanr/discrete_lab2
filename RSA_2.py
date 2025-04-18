import random
from numba import njit
from numba import uint64

@njit
def is_prime(n: uint64) -> bool:
    """
    Check if a number is prime.
    """
    if n <= 1:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

@njit
def return_prime(n: uint64) -> uint64:
    """
    Return the next prime number greater than n.
    """
    if n < 2:
        return 2
    if n % 2 == 0:
        n += 1
    while True:
        if is_prime(n):
            return n
        n += 2
    return -1


def large_prime(bits=512):
    i = random.getrandbits(bits)
    # i |= (1 << bits - 1) | 1  # Ensure the number is odd and has the correct bit length
    i = i | 1  # Ensure the number is odd
    # print(i)
    return return_prime(i)


class RSA:
    def __init__(self):
        keys = self.generate_keys()
        self.public_key, self.private_key = keys


    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a


    def generate_keys(self):
        p = large_prime(55)
        # print(p)
        q = large_prime(55)
        # print(q)

        n = p * q
        f = (p - 1)*(q - 1)

        e = 65537
        while self.gcd(e, f) != 1:
            e += 2

        d = pow(e, -1, f)
        return ((e, n), (d, n))


    def encrypt(self, text, key):
        e, n = key
        txt = []
        for i in text:
            txt.append(pow(ord(i), e, n))
        return txt

    def decrypt(self, ciphertext):
        d, n = self.private_key
        txt = ""
        for i in ciphertext:
            txt += chr(pow(i, d, n))
        return txt
q = RSA()
print(pow(2, -1, 3))