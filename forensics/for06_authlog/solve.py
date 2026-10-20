from pathlib import Path
import re
s=Path(__file__).with_name('auth.log').read_text();line=next(x for x in s.splitlines() if 'Accepted password' in x)
user=re.search(r'Accepted password for (\S+)',line).group(1)
print('SPKctf{'+user+'}')
