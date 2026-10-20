from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
folders=sorted(x for x in root.glob('for[0-9][0-9]_*') if x.is_dir())
errors=[]
for folder in folders:
 r=subprocess.run([sys.executable,str(folder/'verify.py')],text=True,capture_output=True,cwd=folder)
 print(r.stdout.strip() if r.returncode==0 else f'{folder.name}: FAIL\n{r.stderr}')
 if r.returncode:errors.append(folder.name)
print(f'{len(folders)-len(errors)}/{len(folders)} PASS')
if errors:sys.exit(1)
