from pathlib import Path
import struct,re,base64,io
from PIL import Image
raw=Path(__file__).with_name('dns_exfil.pcap').read_bytes();pos=24;parts={}
while pos<len(raw):
 ts,us,n,m=struct.unpack_from('<IIII',raw,pos);pos+=16;pkt=raw[pos:pos+n];pos+=n
 if pkt[23]!=17:continue
 off=14+(pkt[14]&15)*4+8;dns=pkt[off:];q=dns[12:];labels=[];i=0
 while i<len(q) and q[i]:
  z=q[i];labels.append(q[i+1:i+1+z].decode());i+=z+1
 if len(labels)>2 and labels[-3:]==['t','example','com']:
  n,b=labels[0].split('-',1);parts[int(n)]=b.upper()
s=''.join(parts[i] for i in sorted(parts));payload=base64.b32decode(s+'='*((-len(s))%8))
im=Image.open(io.BytesIO(payload));im.verify()
print(re.search(rb'SPKctf\{[^}]+\}',payload).group().decode())
