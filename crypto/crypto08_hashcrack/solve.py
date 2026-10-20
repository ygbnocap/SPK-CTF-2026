import hashlib

db = dict(line.split("=") for line in open("db.txt").read().split())
salt, target = db["salt"], db["hash"]

for word in open("wordlist.txt").read().split():
    if hashlib.sha256((salt + word).encode()).hexdigest() == target:
        print(f"пароль: {word}")
        print(f"SPKctf{{{word}}}")
        break
