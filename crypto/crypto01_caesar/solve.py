import string

def caesar(text, shift):
    res = []
    for ch in text:
        if ch in string.ascii_lowercase:
            res.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        elif ch in string.ascii_uppercase:
            res.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            res.append(ch)
    return "".join(res)

text = open("letter.txt", encoding="utf-8").read()
for shift in range(26):
    dec = caesar(text, -shift)
    if "SPKctf{" in dec:
        print(f"shift={shift}")
        print(dec)
        break
