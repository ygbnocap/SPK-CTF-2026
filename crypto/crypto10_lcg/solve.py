import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import inverse

M = 2**64
s = [int(line.split("=")[1]) for line in open("outputs.txt")
     if line.startswith("s")]

a = ((s[1] - s[2]) * inverse(s[0] - s[1], M)) % M
c = (s[1] - a * s[0]) % M
print(f"a={a}, c={c}")

s7 = (a * s[5] + c) % M
key = hashlib.sha256(str(s7).encode()).digest()

data = open("flag.enc", "rb").read()
iv, ct = data[:16], data[16:]
flag = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ct), 16).decode()
print(flag)
