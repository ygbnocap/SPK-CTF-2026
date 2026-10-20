from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
flag=(p/'flag.txt').read_text().strip()
assert flag in subprocess.check_output([str(p/'runtime')],cwd=p,text=True)
print('PASS')
