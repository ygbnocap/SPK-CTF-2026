import base64
import codecs

FLAG = "SPKctf{3nc0d1ng_is_n0t_crypt0}"

blob = base64.b64encode(codecs.encode(FLAG, "rot_13").encode()).decode()
with open("blob.txt", "w") as f:
    f.write("TVRoZV9jbHVia29r\n" + blob + "\n")
print("blob.txt создан")
