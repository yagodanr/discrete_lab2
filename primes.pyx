# cython: boundscheck=False, wraparound=False, nonecheck=False

from libc.math cimport sqrt
from cython cimport long

cdef inline bint is_prime(unsigned long long n):
    if n <= 1:
        return False
    if n % 2 == 0:
        return n == 2

    cdef unsigned long long i = 3
    while i*i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

cpdef return_prime(unsigned long long n):
    if n % 2 == 0:
        n += 1
    while not is_prime(n):
        n += 2
    return n