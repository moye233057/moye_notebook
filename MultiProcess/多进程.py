import math
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

PRIMES = [112272535095297] * 100


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


def single_thread():
    for number in PRIMES:
        is_prime(number)


def multi_thread():
    with ThreadPoolExecutor() as pool:
        pool.map(is_prime, PRIMES)


def multi_process():
    with ProcessPoolExecutor() as pool:
        pool.map(is_prime, PRIMES)


if __name__ == '__main__':
    start = time.time()
    single_thread()
    end = time.time()
    print("single_thread, cost:", end - start, "seconds")

    start1 = time.time()
    multi_thread()
    end1 = time.time()
    print("multi_thread, cost:", end1 - start1, "seconds")

    start2 = time.time()
    multi_process()
    end2 = time.time()
    print("multi_process, cost:", end2 - start2, "seconds")