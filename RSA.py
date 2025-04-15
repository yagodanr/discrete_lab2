import random
class RSA:
    def __init__(self):
        keys = self.generate_keys()
        self.public_key, self.private_key = keys

    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def generate_keys(self):
        p = self.large_prime()
        q = self.large_prime()
        while q == p:
            q = self.large_prime()

        n = p * q
        f = (p - 1)*(q - 1)

        e = 65537
        while self.gcd(e, f) != 1:
            e += 2

        d = pow(e, -1, f)
        return ((e, n), (d, n))

    def large_prime(self):
        s = list(range(150, 400))
        random.shuffle(s)
        for i in s:
            if self.is_prime(i):
                return i

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