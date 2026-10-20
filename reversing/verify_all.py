import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
for folder in sorted(root.glob('rev[0-9][0-9]_*')):
    print(folder.name, end=': ',flush=True)
    subprocess.run([sys.executable,str(folder/'verify.py')],check=True,cwd=folder)
    solved=subprocess.check_output([sys.executable,str(folder/'solve.py')],text=True,cwd=folder).strip()
    expected=(folder/'flag.txt').read_text().strip()
    assert solved==expected,(folder,solved,expected)
print('ALL TEN PASS — artifact and organizer solution')
