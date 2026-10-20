from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
r=subprocess.run([sys.executable,str(p/'solve.py')],cwd=p,capture_output=True,text=True,check=True)
assert 'SPKctf{r3c0v3r_d3l3t3d_fl4g}' in r.stdout,(r.stdout,r.stderr)
print('for04_disk: PASS')
