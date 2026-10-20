#!/usr/bin/env python3
"""Генератор задания SPK-Crypto-05 «Куб маленького числа».

Создаёт RSA-1024 с открытой экспонентой e=3 и гарантирует m^3 < n.
Зависимости: только стандартная библиотека Python 3.
"""
from math import gcd
from pathlib import Path
import secrets

HERE = Path(__file__).resolve().parent
OUT = HERE / "rsa_params.txt"
FLAG = b"SPKctf{rsa_low_exponent_attack}"
E = 3
BITS = 512


def is_probable_prime(n: int, rounds: int = 40) -> bool:
    """Тест Миллера—Рабина."""
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1
        if gcd(candidate - 1, E) == 1 and is_probable_prime(candidate):
            return candidate


def main() -> None:
    message = int.from_bytes(FLAG, "big")
    while True:
        p = generate_prime(BITS)
        q = generate_prime(BITS)
        if p == q:
            continue
        n = p * q
        # Главная учебная уязвимость: при m^3 < n шифрование по модулю
        # не оборачивает результат, поэтому c == m**3.
        if message ** E < n:
            break

    c = pow(message, E, n)
    assert c == message ** E
    OUT.write_text(
        "# SPK-Crypto-05: RSA parameters\n"
        "# n and c are decimal integers; no private key is provided.\n"
        f"n = {n}\n"
        f"e = {E}\n"
        f"c = {c}\n",
        encoding="utf-8",
    )
    print(f"[+] Created: {OUT}")
    print(f"[+] Modulus size: {n.bit_length()} bits")
    print(f"[+] Public exponent: e={E}")
    print("[+] Ciphertext written to rsa_params.txt")
    print("[+] Organizer check: m^3 < n (vulnerable by design)")


if __name__ == "__main__":
    main()
