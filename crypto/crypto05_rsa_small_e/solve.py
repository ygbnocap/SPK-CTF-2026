#!/usr/bin/env python3
"""Организаторский проверочный решатель SPK-Crypto-05."""
from pathlib import Path
import re

PARAMS = Path(__file__).resolve().parent / "rsa_params.txt"


def integer_cuberoot(n: int) -> int:
    """Точный floor(cuberoot(n)) без сторонних библиотек."""
    if n < 0:
        return -integer_cuberoot(-n)
    if n < 2:
        return n

    lo, hi = 0, 1 << ((n.bit_length() + 2) // 3)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> None:
    values = {}
    for line in PARAMS.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r"(n|e|c)\s*=\s*(\d+)", line)
        if match:
            values[match.group(1)] = int(match.group(2))

    if not {"n", "e", "c"} <= values.keys():
        raise SystemExit("Ошибка: в rsa_params.txt должны быть n, e и c.")

    n, e, c = values["n"], values["e"], values["c"]
    if e != 3:
        raise SystemExit(f"Ожидалось e=3, получено e={e}.")

    m = integer_cuberoot(c)
    if m ** 3 != c:
        raise SystemExit(
            "c не является точным кубом. Проверьте, что генератор создал "
            "уязвимый вариант с m^3 < n."
        )

    raw = m.to_bytes((m.bit_length() + 7) // 8, "big")
    print(raw.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
