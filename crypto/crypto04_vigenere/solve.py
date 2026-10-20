import string

KEY = "judge"
ALPHA = string.ascii_lowercase

def vig(text, key):
    res, ki = [], 0
    for ch in text:
        if ch in ALPHA:
            res.append(ALPHA[(ALPHA.index(ch) - ALPHA.index(key[ki % len(key)])) % 26])
            ki += 1
        else:
            res.append(ch)
    return "".join(res)

for line in open("ciphertext.txt").read().splitlines():
    if line.strip():
        print(vig(line, KEY))
