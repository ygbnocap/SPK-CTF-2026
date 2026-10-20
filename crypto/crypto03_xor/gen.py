FLAG = "SPKctf{s1ngl3_byt3_x0r_key}"
KEY = 0x37

cipher = bytes(b ^ KEY for b in FLAG.encode())
with open("cipher.hex", "w") as f:
    f.write(cipher.hex())
print("cipher.hex создан")
