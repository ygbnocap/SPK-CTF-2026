import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = b"SPKctf{lcg_state_recovery}"
M = 2**64
a = int.from_bytes(os.urandom(8), "big") | 1
c = int.from_bytes(os.urandom(8), "big") | 1  # нечётное: разности выходов всегда нечётные (обратимы mod 2^64)
x = int.from_bytes(os.urandom(8), "big")

outputs = []
for _ in range(6):
    x = (a * x + c) % M
    outputs.append(x)
x7 = (a * x + c) % M          # седьмой выход — ключ
key = hashlib.sha256(str(x7).encode()).digest()
iv = os.urandom(16)
ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(FLAG, 16))

with open("outputs.txt", "w") as f:
    f.write("# LCG: x_{n+1} = (a*x_n + c) mod m\n# m = 2^64\n")
    for i, s in enumerate(outputs):
        f.write(f"s{i+1}={s}\n")
open("flag.enc", "wb").write(iv + ct)
print("outputs.txt, flag.enc созданы")
