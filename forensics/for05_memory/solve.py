from pathlib import Path
import re
raw=Path(__file__).with_name('editor.dmp').read_bytes()
match=re.search(rb'UNSAVED DOCUMENT v3.*?(SPKctf\{[^}]+\})',raw,re.S)
assert match;print(match.group(1).decode())
