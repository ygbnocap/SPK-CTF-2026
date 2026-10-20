from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
flag=(p/'flag.txt').read_text().strip()
assert 'correct' in subprocess.check_output([str(p/'transform')],input=flag+'\n',text=True,cwd=p)
print('PASS')
