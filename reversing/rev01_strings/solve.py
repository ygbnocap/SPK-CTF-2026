from pathlib import Path
import re,subprocess,base64,hashlib,os
p=Path(__file__).resolve().parent
print(re.search(rb"SPKctf\{[^}]+\}",(p/"strings").read_bytes()).group().decode())
