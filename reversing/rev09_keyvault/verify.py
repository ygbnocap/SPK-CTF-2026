from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
flag=(p/'flag.txt').read_text().strip()
from hashlib import sha256
b=(p/'encrypted_flag.bin').read_bytes();key=sha256(b'spkadmin').hexdigest()
r=subprocess.run(['openssl','enc','-d','-aes-256-cbc','-K',key,'-iv',b[:16].hex()],input=b[16:],capture_output=True,check=True)
assert r.stdout.decode()==flag
print('PASS')
