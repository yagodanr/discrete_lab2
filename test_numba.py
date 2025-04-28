from time import time

from numba import njit, prange, uint64


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


def test_return_prime():
    """
    Test the return_prime function.
    """
    # Test with a small number

    # for i in range(2**60+1, 2**62, 2):
    avg_time = []
    i = 2**60 + 1
    while i < 2**61:
        start_time = time()
        result = return_prime(i)
        end_time = time()
        print(f"Test with {i = } passed in {end_time - start_time:.6f} seconds {result = }")
        i = result + 2
        avg_time.append(end_time - start_time)
    avg_time = sum(avg_time) / len(avg_time)
    print(f"Average time taken: {avg_time:.6f} seconds")
    # i = 3799399096626203401
    # start_time = time()
    # result = return_prime(3799399096626203401)
    # end_time = time()
    # print(f"Test with {i = } passed in {end_time - start_time:.6f} seconds {result = }")


if __name__ == "__main__":
    test_return_prime()
