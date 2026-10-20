from pathlib import Path
import re,subprocess,base64,hashlib,os
p=Path(__file__).resolve().parent
src=(p/"src.c").read_text()
a=[int(x) for x in re.search(r"expected\[\]=\{([^}]+)\}",src).group(1).split(",")]
print(bytes(x^0x55 for x in a).decode())
