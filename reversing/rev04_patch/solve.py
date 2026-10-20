from pathlib import Path
import re,subprocess,base64,hashlib,os
p=Path(__file__).resolve().parent
print(subprocess.check_output([str(p/"patch")],env={**os.environ,"MODE":"admin"},text=True).strip())
