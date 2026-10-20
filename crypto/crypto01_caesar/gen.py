import string

FLAG = "SPKctf{caesar_shift_five}"
SHIFT = 5

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

text = ("Dear friend, the meeting is moved to friday. "
        "The cipher shift equals the number of fingers on one hand. "
        "Regards, S.")
enc = caesar(text, SHIFT)
with open("letter.txt", "w", encoding="utf-8") as f:
    f.write(enc + "\n\nP.S. flag: " + caesar(FLAG, SHIFT) + "\n")
print("letter.txt создан")
