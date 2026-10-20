from pathlib import Path
import re,subprocess,base64,hashlib,os
p=Path(__file__).resolve().parent
blob=(p/"encrypted_flag.bin").read_bytes()
key=hashlib.sha256(b"spkadmin").hexdigest()
r=subprocess.run(["openssl","enc","-d","-aes-256-cbc","-K",key,"-iv",blob[:16].hex()],input=blob[16:],capture_output=True,check=True)
print(r.stdout.decode())
