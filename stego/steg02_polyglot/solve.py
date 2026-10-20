import zipfile
z = zipfile.ZipFile("double.jpg")   # zipfile читает архив с конца файла
print(z.read("note.txt").decode())
assert "SPKctf{" in z.read("note.txt").decode()
