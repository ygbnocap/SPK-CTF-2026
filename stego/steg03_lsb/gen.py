"""Steg-03: LSB в RGB, последовательный порядок пикселей."""
import numpy as np
from PIL import Image

FLAG = b"SPKctf{lsb_pixel_channels}"

# 1. cover-изображение (тестовое; можно заменить cover.png своим)
img = np.zeros((150, 200, 3), dtype=np.uint8)
for y in range(150):
    for x in range(200):
        img[y, x] = [(x*5) % 256, (y*7) % 256, ((x*2+y*3)) % 256]
Image.fromarray(img).save("cover.png")

# 2. вшиваем флаг: биты сообщения + нуль-терминатор в LSB каналов RGB
data = np.array(Image.open("cover.png").convert("RGB"), dtype=np.uint8)
bits = "".join(f"{b:08b}" for b in FLAG + b"\x00")
flat = data.reshape(-1)
assert len(bits) <= flat.size, "картинка маленькая для сообщения"
for i, bit in enumerate(bits):
    flat[i] = (flat[i] & 0xFE) | int(bit)
Image.fromarray(flat.reshape(data.shape).astype(np.uint8)).save("pixel.png")
print("pixel.png создан")
