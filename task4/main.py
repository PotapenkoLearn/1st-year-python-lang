import ctypes

MAX = 10_000_000

# Загружаем C-библиотеку
lib = ctypes.CDLL('./libtest.so')


def get_goldbach_sum(primes, number):
    if number < 4 or number % 2 != 0:
        return

    count = 0
    min_prime = 0

    for i in range(2, number // 2 + 1):
        if primes[i] and primes[number - i]:
            if count == 0:
                min_prime = i
            count += 1

    if count:
        print(number, count, min_prime, number - min_prime)


def main():
    n, m = map(int, input("Введите пару чисел (4 <= n < m <= 10000000): ").split())

    if n < 4 or m > MAX or n > m:
        print("Некорректная пара чисел")
        return

    primes = (ctypes.c_int * (m + 1))()
    lib.calculate_primes(primes, m)

    py_primes = [primes[i] for i in range(m + 1)]

    for i in range(n, m + 1):
        get_goldbach_sum(py_primes, i)


if __name__ == "__main__":
    main()

if __name__ == '__main__':
    main()
