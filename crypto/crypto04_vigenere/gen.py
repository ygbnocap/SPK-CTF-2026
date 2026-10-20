import string

FLAG = "SPKctf{vigenere_weak_key}"
KEY = "judge"
ALPHA = string.ascii_lowercase

def vig(text, key, enc=True):
    res, ki = [], 0
    for ch in text:
        if ch in ALPHA:
            shift = ALPHA.index(key[ki % len(key)]) * (1 if enc else -1)
            res.append(ALPHA[(ALPHA.index(ch) + shift) % 26])
            ki += 1
        else:
            res.append(ch)
    return "".join(res)

text = "the flag is hidden below, good luck with the vigenere cipher, it is unbreakable"
with open("ciphertext.txt", "w") as f:
    f.write(vig(text, KEY) + "\n\n" + vig(FLAG.lower(), KEY) + "\n")
print("ciphertext.txt создан")
