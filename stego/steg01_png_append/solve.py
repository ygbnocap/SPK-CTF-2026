data = open("secret.png", "rb").read()
iend = data.rfind(b"IEND") + 8          # конец чанка IEND (+ CRC)
tail = data[iend:]
print(tail.decode(errors="replace"))
assert "SPKctf{" in tail.decode()
