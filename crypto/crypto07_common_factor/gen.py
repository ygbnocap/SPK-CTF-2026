from Crypto.Util.number import getPrime, bytes_to_long, inverse

FLAG = b"SPKctf{rsa_common_factor}"
e = 65537

p  = getPrime(512)
q1 = getPrime(512)
q2 = getPrime(512)
n1, n2 = p * q1, p * q2

c1 = pow(bytes_to_long(FLAG), e, n1)
c2 = pow(bytes_to_long(FLAG), e, n2)

for name, n in [("key1.pub", n1), ("key2.pub", n2)]:
    with open(name, "w") as f:
        f.write(f"e={e}\nn={n}\n")
open("c1.bin", "wb").write(c1.to_bytes((n1.bit_length() + 7) // 8, "big"))
open("c2.bin", "wb").write(c2.to_bytes((n2.bit_length() + 7) // 8, "big"))
print("key1.pub key2.pub c1.bin c2.bin созданы")
