import numpy as np
from PIL import Image

data = np.array(Image.open("pixel.png").convert("RGB")).reshape(-1)
out = bytearray()
for i in range(0, len(data) - 7, 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | (data[i + j] & 1)
    if byte == 0:
        break
    out.append(byte)
print(out.decode())
assert "SPKctf{" in out.decode()
