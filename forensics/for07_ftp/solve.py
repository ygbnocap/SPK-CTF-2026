from pathlib import Path
import io,zipfile,struct,re
raw=Path(__file__).with_name('midnight.pcap').read_bytes();pos=24;data=[]
while pos<len(raw):
 ts,us,n,n0=struct.unpack_from('<IIII',raw,pos);pos+=16;pkt=raw[pos:pos+n];pos+=n
 if pkt[23]!=6:continue
 ip=14+(pkt[14]&15)*4;h=(pkt[ip+12]>>4)*4;body=pkt[ip+h:]
 if body:data.append(body)
ctl=b'\n'.join(data);pw=re.search(rb'PASS (\S+)',ctl).group(1)
arc=next(x for x in data if x.startswith(b'PK\x03\x04'))
with zipfile.ZipFile(io.BytesIO(arc)) as z:print(z.read('secret.txt',pwd=pw).decode().strip())
