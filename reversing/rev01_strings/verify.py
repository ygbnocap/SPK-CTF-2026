from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
flag=(p/'flag.txt').read_text().strip()
assert flag.encode() in (p/'strings').read_bytes()
print('PASS')
