from pathlib import Path
import subprocess,os
p=Path(__file__).resolve().parent
flag=(p/'flag.txt').read_text().strip()
assert flag in subprocess.check_output([str(p/'patch')],env={**os.environ,'MODE':'admin'},text=True)
print('PASS')
