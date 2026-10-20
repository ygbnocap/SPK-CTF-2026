from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

FLAG = b"SPKctf{padding_oracle_exploit}"
key = os.urandom(32)                      # ключ сервиса
iv = os.urandom(16)
ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(FLAG, 16))

open("key.bin", "wb").write(key)          # для сервиса (НЕ выдавать игрокам)
open("iv.bin", "wb").write(iv)            # для сервиса (НЕ выдавать игрокам)
open("flag_ct.bin", "wb").write(iv + ct)  # файл для игроков
print("flag_ct.bin (игрокам), key.bin/iv.bin (только сервису)")
