from pathlib import Path
import re
raw=Path(__file__).with_name('floppy.raw').read_bytes()
assert raw[1024+56:1024+58]==b'\x53\xef','Not EXT2'
print(re.search(rb'SPKctf\{[^}]+\}',raw).group().decode())
