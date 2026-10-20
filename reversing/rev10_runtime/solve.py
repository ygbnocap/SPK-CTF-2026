from pathlib import Path
import re,subprocess,base64,hashlib,os
p=Path(__file__).resolve().parent
src=(p/"src.c").read_text();parts=re.findall(r"static const char p[0-4]\[\]=\"([^\"]+)\"",src);assert len(parts)==5;print("".join(parts))
