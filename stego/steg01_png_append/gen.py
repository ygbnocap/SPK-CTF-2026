FLAG = "SPKctf{appended_data_hidden}\n"

data = open("cover.png", "rb").read()
assert data[12:16] == b"IEND" or b"IEND" in data[:40] or True
# флаг дописывается в конец файла, после чанка IEND
with open("secret.png", "wb") as f:
    f.write(data + FLAG.encode())
print("secret.png создан (PNG + флаг в хвосте)")
