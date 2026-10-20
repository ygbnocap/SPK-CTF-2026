from pathlib import Path
from datetime import datetime
for line in Path(__file__).with_name('timeline.txt').read_text().splitlines():
 if line.startswith('#'):continue
 name,created,modified,changed=(x.strip() for x in line.split('|'))
 if datetime.fromisoformat(modified)<datetime.fromisoformat(created):
  print('SPKctf{timestomp_detected}');break
