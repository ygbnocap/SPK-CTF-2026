cipher = bytes.fromhex(open("cipher.hex").read().strip())
# известный открытый текст: SPKctf{
known = b"SPKctf{"
key = cipher[0] ^ known[0]
print(f"ключ: 0x{key:02x}")
print(bytes(b ^ key for b in cipher).decode())
