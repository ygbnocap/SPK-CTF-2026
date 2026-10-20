from pathlib import Path
import re
s=Path(__file__).with_name('access.log').read_text()
for line in s.splitlines():
 if 'sqlmap' in line or 'union' in line:
  print(re.search(r'SPKctf\{[^}]+\}',line).group())
