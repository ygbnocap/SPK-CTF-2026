from pathlib import Path
import re,subprocess,base64,hashlib,os
p=Path(__file__).resolve().parent
src=(p/"src.c").read_text()
alpha=re.search(r"alphabet\[\]=\"([^\"]+)\"",src).group(1)
enc=re.search(r"encoded\[\]=\"([^\"]+)\"",src).group(1)
std="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
print(base64.b64decode(enc.translate(str.maketrans(alpha,std))).decode())
