import base64
import codecs

text = open("blob.txt").read().strip().splitlines()[-1]
flag = codecs.decode(base64.b64decode(text).decode(), "rot_13")
print(flag)
