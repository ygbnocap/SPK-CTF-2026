import base64
import requests

URL = "http://localhost:8106/encrypt"

def oracle(data: bytes) -> bytes:
    r = requests.get(URL, params={"data": data})
    r.raise_for_status()
    return base64.b64decode(r.text)

BLOCK = 16
secret = b""
while not secret.endswith(b"}"):
    pad_len = BLOCK - 1 - (len(secret) % BLOCK)
    prefix = b"A" * pad_len
    target = oracle(prefix)[: len(prefix) + len(secret) + 1]
    found = False
    for b in range(256):
        if oracle(prefix + secret + bytes([b]))[: len(target)] == target:
            secret += bytes([b])
            found = True
            break
    if not found:
        break
    print(secret.decode())
print("FLAG:", secret.decode())
