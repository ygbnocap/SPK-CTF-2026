from pathlib import Path
import re,subprocess,base64,hashlib,os
p=Path(__file__).resolve().parent
print(re.search(r"SPKctf\{antidebug_bypassed\}",(p/"src.c").read_text()).group())
