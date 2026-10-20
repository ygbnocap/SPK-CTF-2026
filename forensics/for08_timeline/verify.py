from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
r=subprocess.run([sys.executable,str(p/'solve.py')],cwd=p,capture_output=True,text=True,check=True)
assert 'SPKctf{timestomp_detected}' in r.stdout,(r.stdout,r.stderr)
print('for08_timeline: PASS')
