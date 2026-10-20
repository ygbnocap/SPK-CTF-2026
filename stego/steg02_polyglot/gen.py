import zipfile
from PIL import Image
import numpy as np

FLAG = "SPKctf{jpeg_zip_polyglot}"

# 1. картинка (тестовая, можно заменить photo.jpg своей)
img = np.zeros((100, 140, 3), dtype=np.uint8)
for y in range(100):
    for x in range(140):
        img[y, x] = [255 - (x*2) % 256, (y*3) % 256, 128]
Image.fromarray(img).save("photo.jpg", quality=90)

# 2. архив с флагом
with zipfile.ZipFile("hidden.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("note.txt", "You found the second bottom!\n" + FLAG + "\n")

# 3. склейка: JPEG + ZIP
with open("double.jpg", "wb") as out:
    out.write(open("photo.jpg", "rb").read())
    out.write(open("hidden.zip", "rb").read())
print("double.jpg создан (JPEG + ZIP)")
