from pathlib import Path
import struct,urllib.parse
raw=Path(__file__).with_name('traffic.pcap').read_bytes();p=24
while p<len(raw):
 ts,ms,n,orig=struct.unpack_from('<IIII',raw,p);p+=16;pkt=raw[p:p+n];p+=n
 off=14+(pkt[14]&15)*4
 if pkt[23]!=6:continue
 start=off+((pkt[off+12]>>4)*4);data=pkt[start:]
 if b'POST /login ' in data:
  form=urllib.parse.parse_qs(data.split(b'\r\n\r\n',1)[1].decode())
  print('SPKctf{'+form['username'][0]+'_'+form['password'][0]+'}')
