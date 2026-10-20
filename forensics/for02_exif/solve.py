from PIL import Image
from pathlib import Path
import re
exif=Image.open(Path(__file__).with_name('photo.jpg')).getexif()
for val in exif.values():
 if isinstance(val,bytes): val=val.decode('latin1','replace')
 m=re.search(r'SPKctf\{[^}]+\}',str(val))
 if m:print(m.group());break
else:raise RuntimeError('EXIF flag missing')
