import base64
import requests
from Crypto.Util.Padding import unpad

URL = "http://localhost:8109/check"
data = open("flag_ct.bin", "rb").read()
iv, ct = data[:16], data[16:]

def oracle(iv: bytes, ct: bytes) -> bool:
    r = requests.get(URL, params={"iv": base64.b64encode(iv),
                                  "ct": base64.b64encode(ct)}, timeout=10)
    return r.status_code == 200

BLOCKS = [ct[i:i+16] for i in range(0, len(ct), 16)]
prev = iv
plaintext = b""
for block in BLOCKS:
    recovered = bytearray(16)
    for pos in range(15, -1, -1):
        pad_val = 16 - pos
        crafted = bytearray(16)
        for k in range(pos + 1, 16):
            crafted[k] = prev[k] ^ recovered[k] ^ pad_val
        for guess in range(256):
            crafted[pos] = guess
            if oracle(bytes(crafted), block):
                # проверка на ложное срабатывание (pad_val == 1)
                if pad_val == 1:
                    crafted2 = bytearray(crafted); crafted2[pos-1] ^= 1
                    if not oracle(bytes(crafted2), block):
                        continue
                recovered[pos] = guess ^ prev[pos] ^ pad_val
                break
    plaintext += bytes(recovered)
    prev = block
    print(plaintext.decode(errors="replace"))

plaintext = unpad(plaintext, 16)
print("FLAG:", plaintext.decode())
