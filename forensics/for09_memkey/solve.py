from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
import re
p=Path(__file__).resolve().parent
key=bytes.fromhex(re.search(rb'KEY: ([0-9a-f]{64})',(p/'vault.dmp').read_bytes()).group(1).decode())
raw=(p/'vault.enc').read_bytes();iv,ct=raw[:16],raw[16:]
d=Cipher(algorithms.AES(key),modes.CBC(iv)).decryptor();pt=d.update(ct)+d.finalize();un=padding.PKCS7(128).unpadder();print((un.update(pt)+un.finalize()).decode())
