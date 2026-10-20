from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
flag=(p/'flag.txt').read_text().strip()
assert 'correct' in subprocess.check_output([str(p/'custom64')],input=next(__import__('re').finditer(r'const char encoded\[\]=\"([^\"]+)', (p/'src.c').read_text())).group(1)+'\n',text=True,cwd=p)
print('PASS')
