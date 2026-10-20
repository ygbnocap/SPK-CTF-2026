import os,struct,socket,random,base64,io,zipfile,hashlib,subprocess,zlib,re,json,textwrap,shutil
from pathlib import Path
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
R=Path(__file__).resolve().parent; rng=random.Random(20261020)
F=['fl4g_in_pl4in_s1ght','3xif_m3t4d4t4_reveals','captured_http_credentials','r3c0v3r_d3l3t3d_fl4g','m3m0ry_dump_s3cr3t','bruteforce_source_detected','ftp_data_exfiltration','timestomp_detected','process_memory_forensics','dns_exfiltration_traced']
D=['for01_logs','for02_exif','for03_pcap','for04_disk','for05_memory','for06_authlog','for07_ftp','for08_timeline','for09_memkey','for10_dns']
for d in D:(R/d).mkdir(exist_ok=True)
def flag(i):return 'SPKctf{'+F[i-1]+'}'
def write(i,name,data):
 p=R/D[i-1]/name
 if isinstance(data,str):p.write_text(data,encoding='utf-8')
 else:p.write_bytes(data)
 return p
def solve_code(i,src):write(i,'solve.py',textwrap.dedent(src).lstrip())
def ver(i):
 write(i,'verify.py',f'''from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
r=subprocess.run([sys.executable,str(p/'solve.py')],cwd=p,capture_output=True,text=True,check=True)
assert {flag(i)!r} in r.stdout,(r.stdout,r.stderr)
print('{D[i-1]}: PASS')
''')
# pcap helper
class PCAP:
 def __init__(self):self.packets=[]
 def append(self,p,sec=0):self.packets.append((1760950000+sec, p))
 def finish(self):
  data=struct.pack('<IHHIIII',0xa1b2c3d4,2,4,0,0,65535,1)
  for ts,p in self.packets:data+=struct.pack('<IIII',ts,0,len(p),len(p))+p
  return data

def checksum(b):
 if len(b)%2:b+=b'\0'
 s=sum(struct.unpack('!%dH'%(len(b)//2),b));s=(s&65535)+(s>>16);s=(s&65535)+(s>>16)
 return (~s)&65535

def packet(src,dst,sport,dport,payload,proto='tcp',seq=1,ack=1,flags=0x18,ident=1):
 a=socket.inet_aton(src);b=socket.inet_aton(dst)
 if proto=='tcp':
  head=struct.pack('!HHIIHHHH',sport,dport,seq,ack,(5<<12)|flags,8192,0,0)
  pseudo=a+b+struct.pack('!BBH',0,6,len(head)+len(payload));cs=checksum(pseudo+head+payload)
  transport=struct.pack('!HHIIHHHH',sport,dport,seq,ack,(5<<12)|flags,8192,cs,0);pr=6
 else:
  head=struct.pack('!HHHH',sport,dport,8+len(payload),0);pseudo=a+b+struct.pack('!BBH',0,17,len(head)+len(payload));cs=checksum(pseudo+head+payload)
  transport=struct.pack('!HHHH',sport,dport,8+len(payload),cs);pr=17
 ip=struct.pack('!BBHHHBBH4s4s',0x45,0,20+len(transport)+len(payload),ident,0x4000,64,pr,0,a,b)
 ip=ip[:10]+struct.pack('!H',checksum(ip))+ip[12:]
 return bytes.fromhex('aabbccddeeff0011223344550800')+ip+transport+payload

def pcap_payloads(fn,proto=None):
 raw=fn.read_bytes();pos=24
 while pos+16<=len(raw):
  _,_,sz,_=struct.unpack_from('<IIII',raw,pos);pos+=16
  p=raw[pos:pos+sz];pos+=sz
  if len(p)<34 or p[12:14]!=b'\x08\x00':continue
  ihl=(p[14]&15)*4;pr=p[23];off=14+ihl
  if pr==6 and len(p)>=off+20:
   h=(p[off+12]>>4)*4;yield 6,p[26:30],p[30:34],p[off+20 if False else off+h:]
  elif pr==17 and len(p)>=off+8:yield 17,p[26:30],p[30:34],p[off+8:]
# 01
lines=[]
for j in range(5000):
 ip=f'192.0.2.{rng.randrange(1,250)}';lines.append(f'20/Oct/2026:09:{j%60:02d}:01 +0000 {ip} "GET /assets/{rng.randrange(1000)}.css HTTP/1.1" 200 1432 "Mozilla/5.0"')
lines.insert(3281,f'20/Oct/2026:09:56:42 +0000 198.51.100.42 "GET /admin_backup?query=union%20select&debug={flag(1)} HTTP/1.1" 200 114 "sqlmap/1.8"')
write(1,'access.log','\n'.join(lines)+'\n');solve_code(1,'''from pathlib import Path
import re
s=Path(__file__).with_name('access.log').read_text()
for line in s.splitlines():
 if 'sqlmap' in line or 'union' in line:
  print(re.search(r'SPKctf\\{[^}]+\\}',line).group())
''')
# 02
im=Image.open(R/'for02_exif'/'source_123.jpg');ex=im.getexif();ex[270]='SPKashka photograph. '+flag(2);ex[315]='SPKashka';ex[37510]=b'ASCII\x00\x00\x00'+flag(2).encode()
im.save(R/D[1]/'photo.jpg',quality=95,exif=ex)
solve_code(2,'''from PIL import Image
from pathlib import Path
import re
exif=Image.open(Path(__file__).with_name('photo.jpg')).getexif()
for val in exif.values():
 if isinstance(val,bytes): val=val.decode('latin1','replace')
 m=re.search(r'SPKctf\\{[^}]+\\}',str(val))
 if m:print(m.group());break
else:raise RuntimeError('EXIF flag missing')
''')
#03
p=PCAP()
for j in range(7):p.append(packet('10.10.0.12','10.10.0.20',54220+j,80,f'GET /assets/{j}.js HTTP/1.1\r\nHost: school.local\r\n\r\n'.encode(),seq=1000+j*200),j)
body=b'username=captured_http&password=credentials'
req=b'POST /login HTTP/1.1\r\nHost: school.local\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: '+str(len(body)).encode()+b'\r\n\r\n'+body
p.append(packet('10.10.0.12','10.10.0.20',54321,80,req,seq=1200),9)
write(3,'traffic.pcap',p.finish())
solve_code(3,'''from pathlib import Path
import struct,urllib.parse
raw=Path(__file__).with_name('traffic.pcap').read_bytes();p=24
while p<len(raw):
 ts,ms,n,orig=struct.unpack_from('<IIII',raw,p);p+=16;pkt=raw[p:p+n];p+=n
 off=14+(pkt[14]&15)*4
 if pkt[23]!=6:continue
 start=off+((pkt[off+12]>>4)*4);data=pkt[start:]
 if b'POST /login ' in data:
  form=urllib.parse.parse_qs(data.split(b'\\r\\n\\r\\n',1)[1].decode())
  print('SPKctf{'+form['username'][0]+'_'+form['password'][0]+'}')
''')
#04 ext2 image minimal
size=8*1024*1024;img=bytearray(size);bs=1024
blk=lambda n:n*bs
payload=(b'RECOVERED EXAM DOCUMENT\nAnswers are still in deleted data blocks\n'+flag(4).encode()+b'\n')
img[blk(22):blk(22)+len(payload)]=payload
# superblock
sup=1024
for off,typ,val in [(0,'I',8192//8),(4,'I',8192),(8,'I',0),(12,'I',8192-23),(16,'I',1013),(20,'I',1),(24,'I',0),(28,'I',0),(32,'I',8192),(36,'I',8192),(40,'I',1024),(44,'I',1760950000),(48,'I',1760950000),(52,'H',0),(54,'H',20),(56,'H',0xef53),(58,'H',1),(60,'H',1),(76,'I',1),(84,'I',11),(88,'H',128),(90,'H',0)]:struct.pack_into('<'+typ,img,sup+off,val)
# group descriptor 2
for off,val in [(0,3),(4,4),(8,5),(12,8192-23),(14,1013),(16,2)]:struct.pack_into('<'+('H' if off>=12 else 'I'),img,blk(2)+off,val)
# bitmaps
for b in range(23):img[blk(3)+b//8]|=1<<(b%8)
for ino in range(11):img[blk(4)+ino//8]|=1<<(ino%8)
# inode root at inode 2, directory block21
inode=blk(5)+128
for off,typ,val in [(0,'H',0x41ed),(4,'I',1024),(8,'I',1760950000),(12,'I',1760950000),(16,'I',1760950000),(26,'H',2),(28,'I',2),(40,'I',21)]:struct.pack_into('<'+typ,img,inode+off,val)
# directory entries
pos=blk(21)
struct.pack_into('<IHBB',img,pos,2,12,1,2);img[pos+8:pos+9]=b'.'
struct.pack_into('<IHBB',img,pos+12,2,1012,2,2);img[pos+20:pos+22]=b'..'
# old deleted inode 12 unallocated with data pointer preserved
old=blk(5)+11*128
for off,typ,val in [(0,'H',0x81a4),(4,'I',len(payload)),(8,'I',1760950000),(16,'I',1760950000),(20,'I',1760950010),(26,'H',0),(28,'I',2),(40,'I',22)]:struct.pack_into('<'+typ,img,old+off,val)
write(4,'floppy.raw',img)
solve_code(4,'''from pathlib import Path
import re
raw=Path(__file__).with_name('floppy.raw').read_bytes()
assert raw[1024+56:1024+58]==b'\\x53\\xef','Not EXT2'
print(re.search(rb'SPKctf\\{[^}]+\\}',raw).group().decode())
''')
#05
content=bytearray(rng.randbytes(70000))
for v,f in [(1,'SPKctf{old_draft_decoy}'),(2,'SPKctf{revised_draft_decoy}'),(3,flag(5))]:
 txt=f'\n-- UNSAVED DOCUMENT v{v} --\nDocument revision={v}\nExam working draft\n{f}\n-- END DOCUMENT --\n'.encode();idx=6000+v*20000;content[idx:idx+len(txt)]=txt
write(5,'editor.dmp',content)
solve_code(5,'''from pathlib import Path
import re
raw=Path(__file__).with_name('editor.dmp').read_bytes()
match=re.search(rb'UNSAVED DOCUMENT v3.*?(SPKctf\\{[^}]+\\})',raw,re.S)
assert match;print(match.group(1).decode())
''')
#06
lines=[]
for j in range(3000):lines.append(f'Oct 20 11:{j%60:02d}:12 spk sshd[{4100+j}]: Failed password for invalid user {rng.choice(["admin","guest","root","test"])} from 203.0.113.77 port {20000+j%2000} ssh2')
lines.insert(2899,'Oct 20 11:59:59 spk sshd[9000]: Accepted password for '+F[5]+' from 203.0.113.77 port 49281 ssh2')
write(6,'auth.log','\n'.join(lines)+'\n')
solve_code(6,'''from pathlib import Path
import re
s=Path(__file__).with_name('auth.log').read_text();line=next(x for x in s.splitlines() if 'Accepted password' in x)
user=re.search(r'Accepted password for (\\S+)',line).group(1)
print('SPKctf{'+user+'}')
''')
#07
p=PCAP();pw='archive42';inner=io.BytesIO()
# zip -P uses trad encryption
work=R/D[6];(work/'secret.txt').write_text(flag(7)+'\n');subprocess.run(['zip','-q','-P',pw,'backup.zip','secret.txt'],cwd=work,check=True)
z=(work/'backup.zip').read_bytes();(work/'secret.txt').unlink();(work/'backup.zip').unlink()
flow=[b'220 FTP service ready\r\n',b'USER student\r\n',b'331 Password required\r\n',b'PASS archive42\r\n',b'230 Login successful\r\n',b'TYPE I\r\n',b'PASV\r\n',b'227 Entering Passive Mode (10,20,0,2,195,80)\r\n',b'RETR backup.zip\r\n',b'150 Opening BINARY mode data connection\r\n']
for j,msg in enumerate(flow):
 src,dst,sp,dp=('10.20.0.1','10.20.0.2',50000,21) if j%2 else ('10.20.0.2','10.20.0.1',21,50000)
 p.append(packet(src,dst,sp,dp,msg,seq=1200+j*100),j)
p.append(packet('10.20.0.2','10.20.0.1',50000,50001,z,seq=9000),15)
write(7,'midnight.pcap',p.finish())
solve_code(7,'''from pathlib import Path
import io,zipfile,struct,re
raw=Path(__file__).with_name('midnight.pcap').read_bytes();pos=24;data=[]
while pos<len(raw):
 ts,us,n,n0=struct.unpack_from('<IIII',raw,pos);pos+=16;pkt=raw[pos:pos+n];pos+=n
 if pkt[23]!=6:continue
 ip=14+(pkt[14]&15)*4;h=(pkt[ip+12]>>4)*4;body=pkt[ip+h:]
 if body:data.append(body)
ctl=b'\\n'.join(data);pw=re.search(rb'PASS (\\S+)',ctl).group(1)
arc=next(x for x in data if x.startswith(b'PK\\x03\\x04'))
with zipfile.ZipFile(io.BytesIO(arc)) as z:print(z.read('secret.txt',pwd=pw).decode().strip())
''')
#08
lines=['# name | created | modified (mtime) | metadata changed (ctime)']
for j in range(20):
 name=f'course/material_{j:02d}.md';ctime=f'2026-09-{j%25+1:02d} 12:00';lines.append(f'{name} | {ctime} | {ctime} | {ctime}')
lines.insert(12,'journal_final.xlsx | 2026-10-19 16:43 | 2024-01-05 03:11 | 2026-10-20 09:16')
write(8,'timeline.txt','\n'.join(lines)+'\n')
solve_code(8,'''from pathlib import Path
from datetime import datetime
for line in Path(__file__).with_name('timeline.txt').read_text().splitlines():
 if line.startswith('#'):continue
 name,created,modified,changed=(x.strip() for x in line.split('|'))
 if datetime.fromisoformat(modified)<datetime.fromisoformat(created):
  print('SPKctf{timestomp_detected}');break
''')
#09
key=rng.randbytes(32);iv=rng.randbytes(16);pt=flag(9).encode();pad=padding.PKCS7(128).padder();padded=pad.update(pt)+pad.finalize()
encryptor=Cipher(algorithms.AES(key),modes.CBC(iv)).encryptor();ct=encryptor.update(padded)+encryptor.finalize()
write(9,'vault.enc',iv+ct)
mem=bytearray(rng.randbytes(30000));tag=b'\nVAULT PROCESS -- crypto state\nKEY: '+key.hex().encode()+b'\nACTIVE: True\n';mem[17300:17300+len(tag)]=tag
write(9,'vault.dmp',mem)
solve_code(9,'''from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
import re
p=Path(__file__).resolve().parent
key=bytes.fromhex(re.search(rb'KEY: ([0-9a-f]{64})',(p/'vault.dmp').read_bytes()).group(1).decode())
raw=(p/'vault.enc').read_bytes();iv,ct=raw[:16],raw[16:]
d=Cipher(algorithms.AES(key),modes.CBC(iv)).decryptor();pt=d.update(ct)+d.finalize();un=padding.PKCS7(128).unpadder();print((un.update(pt)+un.finalize()).decode())
''')
#10 create tiny png with flag as tEXt chunk
im=Image.new('RGB',(24,24),(30,80,150));buffer=io.BytesIO();im.save(buffer,format='PNG');raw=buffer.getvalue();
def pngchunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
pos=raw.index(b'IEND')-4
raw=raw[:pos]+pngchunk(b'tEXt',b'SPK message\x00'+flag(10).encode())+raw[pos:]
enc=base64.b32encode(raw).decode().rstrip('=');segments=[enc[i:i+35] for i in range(0,len(enc),35)]
p=PCAP();rng.shuffle(segments) if False else None
order=list(range(len(segments)));rng.shuffle(order)
for k,index in enumerate(order):
 domain=f'{index}-{segments[index].lower()}.t.example.com';q=bytes([len(x) for x in []]);q=b''.join(bytes([len(part)])+part.encode() for part in domain.split('.'))+b'\x00'
 dns=struct.pack('!HHHHHH',1400+k,0x0100,1,0,0,0)+q+struct.pack('!HH',1,1)
 p.append(packet('10.5.0.3','8.8.8.8',31000+k,53,dns,proto='udp',ident=k+1),k)
write(10,'dns_exfil.pcap',p.finish())
solve_code(10,'''from pathlib import Path
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
print(re.search(rb'SPKctf\\{[^}]+\\}',payload).group().decode())
''')
for i in range(1,11):ver(i)
write(1,'../verify_all.py','''from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
folders=sorted(x for x in root.glob('for[0-9][0-9]_*') if x.is_dir())
errors=[]
for folder in folders:
 r=subprocess.run([sys.executable,str(folder/'verify.py')],text=True,capture_output=True,cwd=folder)
 print(r.stdout.strip() if r.returncode==0 else f'{folder.name}: FAIL\\n{r.stderr}')
 if r.returncode:errors.append(folder.name)
print(f'{len(folders)-len(errors)}/{len(folders)} PASS')
if errors:sys.exit(1)
''')
(R/'FLAG_REFERENCE_ORGANIZER_ONLY.txt').write_text('\n'.join(f'{D[i-1]} {flag(i)}' for i in range(1,11))+'\n')
(R/'README_ORGANIZER.md').write_text('''# SPK Forensics 01–10 — организаторский комплект

Игрокам выдавать только артефакты, не выдавать solve.py, verify.py или файл флагов.

| ID | Файл игрока | Механика |
| --- | --- | --- |
| For-01 | for01_logs/access.log | поиски аномального HTTP-запроса |
| For-02 | for02_exif/photo.jpg | EXIF ImageDescription, ваша фотография 123.jpg |
| For-03 | for03_pcap/traffic.pcap | HTTP POST форма, TCP/IPv4 PCAP |
| For-04 | for04_disk/floppy.raw | ext2-подобный образ с удалённым inode и остаточными данными |
| For-05 | for05_memory/editor.dmp | три версии несохранённого документа |
| For-06 | for06_authlog/auth.log | SSH-аудит, одобренный вход |
| For-07 | for07_ftp/midnight.pcap | FTP credentials и ZIP в data-потоке |
| For-08 | for08_timeline/timeline.txt | аномальные отметки времени |
| For-09 | for09_memkey/vault.dmp + vault.enc | AES-256-CBC и ключ в памяти |
| For-10 | for10_dns/dns_exfil.pcap | DNS-метки base32 + восстановление PNG |

Проверка: `python3 verify_all.py`. Python: требуется `Pillow` и `cryptography`.

Особенности: For-04 — учебный ext2-образ, структура суперблока/инодов создаётся вручную. Рекомендуется дополнительно проверить `fsck.ext2` и `debugfs` на VPS перед публикацией. For-06 и For-08 в исходном пакете имеют противоречия между форматом вычисляемого флага и точным фиксированным флагом; здесь приоритет имеет точный флаг раздела 7. For-10 содержит PNG в виде base32 по DNS-запросам; флаг расположен в PNG tEXt. Пакеты PCAP сгенерированы вручную с контрольными суммами.
''')
print('Built',R)
