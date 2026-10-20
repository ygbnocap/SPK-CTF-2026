from math import gcd
from Crypto.Util.number import long_to_bytes, inverse

def read_pub(name):
    vals = dict(line.split("=") for line in open(name).read().split())
    return int(vals["e"]), int(vals["n"])

e1, n1 = read_pub("key1.pub")
e2, n2 = read_pub("key2.pub")
c1 = int.from_bytes(open("c1.bin", "rb").read(), "big")

p = gcd(n1, n2)
assert p != 1, "общего делителя нет"
q1 = n1 // p
phi = (p - 1) * (q1 - 1)
d = inverse(e1, phi)
m = pow(c1, d, n1)
flag = long_to_bytes(m).decode()
print(flag)
