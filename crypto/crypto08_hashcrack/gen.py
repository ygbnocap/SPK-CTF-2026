import hashlib
import random
import string

WORDS = [
    "123456", "password", "12345678", "qwerty", "abc123", "football",
    "monkey", "letmein", "dragon", "111111", "baseball", "iloveyou",
    "trustno1", "sunshine", "master", "welcome1", "shadow", "ashley",
    "michael", "ninja", "mustang", "access", "flower", "hottie",
]
password = "sunshine"  # фиксировано: флаг = SPKctf{sunshine}
salt = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
h = hashlib.sha256((salt + password).encode()).hexdigest()

with open("db.txt", "w") as f:
    f.write(f"user=admin\nsalt={salt}\nhash={h}\n")
with open("wordlist.txt", "w") as f:
    f.write("\n".join(WORDS) + "\n")
print("db.txt, wordlist.txt созданы")
