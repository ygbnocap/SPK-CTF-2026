#!/usr/bin/env python3
"""SPK.ctf-2026 CTFd API importer: conservative upsert, no hint operations."""
import argparse, hashlib, json, os, re, sys, time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    sys.exit('Установите зависимость: python3 -m pip install requests')

SCORES={'Easy':(100,30,40),'Easy-Medium':(200,25,80),'Medium':(300,20,120),'Hard':(400,15,160),'Insane':(500,10,200)}
FOLDER={'WEB':'web','Crypto':'crypto','For':'forensics','Steg':'stego','Rev':'reversing'}
REV_NAMES={1:'strings',2:'check',3:'xorlock',4:'patch',5:'transform',6:'custom64',7:'vm',8:'antidebug',9:'keyvault',10:'runtime'}

class API:
    def __init__(self, url, token, insecure=False):
        self.base=url.rstrip('/')+'/api/v1'; self.s=requests.Session(); self.s.headers.update({'Authorization':'Token '+token, 'Accept':'application/json'})
        self.s.verify=not insecure
    def request(self, verb, route, **kw):
        for attempt in range(3):
            # This CTFd instance requires JSON Content-Type even on authenticated GETs.
            # Multipart uploads must let requests generate its own boundary.
            extra_headers = dict(kw.pop('headers', {}))
            if 'files' not in kw:
                extra_headers.setdefault('Content-Type', 'application/json')
            r=self.s.request(verb,self.base+route,timeout=45,headers=extra_headers,allow_redirects=False,**kw)
            if r.status_code in (429,502,503,504) and attempt<2:
                time.sleep(2*(attempt+1)); continue
            try: j=r.json()
            except ValueError: raise RuntimeError(f'{verb} {route}: HTTP {r.status_code}: {r.text[:250]}')
            if not r.ok or not j.get('success',False): raise RuntimeError(f'{verb} {route}: HTTP {r.status_code}: {str(j)[:900]}')
            return j.get('data')
    def get(self,route): return self.request('GET',route)
    def post(self,route,**kw): return self.request('POST',route,**kw)
    def patch(self,route,payload): return self.request('PATCH',route,json=payload)

def parse(src):
    text=src.read_text(encoding='utf-8'); headers=list(re.finditer(r'^### SPK-(WEB|Crypto|For|Steg|Rev)-(\d\d)\.\s*(.+?)\s*$',text,re.M)); items=[]
    for idx,m in enumerate(headers):
        block=text[m.end():headers[idx+1].start() if idx+1<len(headers) else text.find('## Сводная таблица',m.end())]
        def field(key):
            z=re.search(r'^\*\*'+re.escape(key)+r'\.\s*[^*]+\*\*\s*(.+)$',block,re.M)
            return z.group(1).strip() if z else None
        rating=field('3'); level=(rating or '').split('—')[0].strip()
        desc=re.search(r'\*\*4\. Описание для игроков:\*\*\s*\n(.*?)\n\s*\*\*5\.',block,re.S)
        f=re.search(r'\*\*7\. Точный флаг:\*\*\s*`(SPKctf\{[^}]+\})`',block)
        if not (level in SCORES and desc and f): raise ValueError(f'Неполная карточка SPK-{m.group(1)}-{m.group(2)}')
        cat={'WEB':'Web','Crypto':'Crypto','For':'Forensics','Steg':'Steganography','Rev':'Reverse Engineering'}[m.group(1)]
        label=m.group(3).strip(); token=m.group(1); n=int(m.group(2)); uid=f'SPK-{token}-{n:02}'
        description=desc.group(1).strip()
        # Don't publish organizer solution, hints or the original markdown file paths.
        items.append(dict(uid=uid,token=token,n=n,name=label,legacy_name=f'{uid}. {label}',category=cat,
            description=description,flag=f.group(1),points=SCORES[level],difficulty=level))
    if len(items)!=50 or len({x['uid'] for x in items})!=50: raise ValueError(f'Ожидалось 50 уникальных заданий, найдено {len(items)}')
    return items

def find_files(x,root):
    group=FOLDER[x['token']]; n=x['n']; dirs=sorted((root/group).glob(f'{group[:3] if group=="crypto" else ""}*')) if False else None
    patterns={'Crypto':f'crypto{n:02}_*','For':f'for{n:02}_*','Steg':f'steg{n:02}_*','Rev':f'rev{n:02}_*'}
    if x['token']=='WEB':return []
    folder=root/group
    matches=list(folder.glob(patterns[x['token']])) if folder.exists() else []
    if len(matches)!=1:return []
    d=matches[0]
    if x['token']=='Crypto':
        files={1:['letter.txt'],2:['blob.txt'],3:['cipher.hex'],4:['ciphertext.txt'],5:['rsa_params.txt'],6:[],7:['key1.pub','key2.pub','c1.bin','c2.bin'],8:['db.txt','wordlist.txt'],9:['flag_ct.bin'],10:['outputs.txt','flag.enc']}[n]
    elif x['token']=='For':
        files={1:['access.log'],2:['photo.jpg'],3:['traffic.pcap'],4:['floppy.raw'],5:['editor.dmp'],6:['auth.log'],7:['midnight.pcap'],8:['timeline.txt'],9:['vault.dmp','vault.enc'],10:['dns_exfil.pcap']}[n]
    elif x['token']=='Steg': files={1:['secret.png'],2:['double.jpg'],3:['pixel.png'],4:['radio.wav'],5:['photo.jpg'],6:['contract.pdf'],7:['campus.png'],8:['rgb.png'],9:['deep.wav'],10:['palette.png']}[n]
    else:files=[REV_NAMES[n]]+(['encrypted_flag.bin'] if n==9 else [])
    return [d/f for f in files if (d/f).is_file()]

def existing_all(api):
    """CTFd /challenges returns the complete list; `page` may be ignored.

    Don't iterate page=1..N until empty: on this instance it returns the same
    nonempty list indefinitely. The SPK importer targets only 50 challenges.
    """
    chunk = api.get('/challenges')
    if isinstance(chunk, list):
        data = chunk
    elif isinstance(chunk, dict):
        data = chunk.get('results', chunk.get('challenges', []))
    else:
        raise RuntimeError('Неожиданный ответ GET /challenges: нужен список заданий')
    if not isinstance(data, list):
        raise RuntimeError('GET /challenges вернул некорректный формат списка')
    # Guard against accidental duplicate entries in a customized API.
    seen = set()
    result = []
    for item in data:
        cid = item.get('id')
        if cid not in seen:
            seen.add(cid)
            result.append(item)
    return result

# Accept both historical names with category/ID prefix and clean names.
# Match only within the same category, fail closed on ambiguous duplicates.
NAME_PREFIX = re.compile(r'^SPK-(?:WEB|Crypto|For|Steg|Rev)-\d{2}\.\s*', re.I)

def clean_name(value):
    return NAME_PREFIX.sub('', str(value or '')).strip()

def match(items, actual):
    claims = {}
    conflicts = []
    used_ids = set()
    for x in items:
        candidates = [z for z in actual
                      if z.get('category') == x['category']
                      and clean_name(z.get('name')) == x['name']]
        if len(candidates) == 1:
            cid = candidates[0].get('id')
            if cid in used_ids:
                conflicts.append(x['uid'])
            else:
                claims[x['uid']] = candidates[0]
                used_ids.add(cid)
        elif len(candidates) > 1:
            conflicts.append(x['uid'])
    return claims, conflicts

def connection(x,host):
    port=8000+x['n'] if x['token']=='WEB' else (8106 if x['token']=='Crypto' and x['n']==6 else 8109 if x['token']=='Crypto' and x['n']==9 else None)
    if port is None:return ''
    url=f'http://{host}:{port}'
    if x['token']=='Crypto': return url+('/encrypt?data=' if x['n']==6 else '/check?iv=...&ct=...')
    return url+({4:'/profile',6:'/fetch',7:'/search',9:'/hello?name='}.get(x['n'],'/'))

def main():
    ap=argparse.ArgumentParser(description='Безопасная синхронизация 50 задач SPK.ctf с CTFd')
    ap.add_argument('--package',type=Path,default=Path(__file__).with_name('SPK_ctf_package.md'))
    ap.add_argument('--root',type=Path,default=Path.home()/'spk-ctf')
    ap.add_argument('--url',default=os.environ.get('CTFD_URL','http://127.0.0.1:8000'))
    ap.add_argument('--host',default='192.168.0.46',help='IP лабораторных сервисов, достижимый игрокам')
    ap.add_argument('--apply',action='store_true',help='Разрешить создание/обновление после dry-run')
    ap.add_argument('--insecure',action='store_true',help='Только если внутренний сертификат CA пока недоверенный')
    ap.add_argument('--allow-update-solved',action='store_true',help='Разрешить обновление заданий с решениями; менять тип по-прежнему нельзя')
    ap.add_argument('--upload-files',action='store_true',help='Добавлять только недостающие файлы, без удаления')
    args=ap.parse_args(); items=parse(args.package); root=args.root.expanduser().resolve()
    token=os.environ.get('CTFD_TOKEN')
    if not token:sys.exit('Не задан CTFD_TOKEN (прочитай README_IMPORT.md)')
    api=API(args.url,token,args.insecure)
    actual=existing_all(api); claims,conflicts=match(items,actual)
    if conflicts:sys.exit('Неоднозначные совпадения: '+', '.join(conflicts))
    types=api.get('/challenges/types')
    if 'dynamic' not in types:sys.exit('Тип dynamic отсутствует в CTFd — сначала включи соответствующий плагин.')
    plan=[]
    for x in items:
        old=claims.get(x['uid']); files=find_files(x,root); expected={p.name for p in files}
        if old:
            full=api.get(f"/challenges/{old['id']}"); solved=int(full.get('solves') or old.get('solves') or 0)
            typ=full.get('type',old.get('type'))
            if typ!='dynamic':action='BLOCKED_TYPE_CHANGE'
            elif solved and not args.allow_update_solved: action='BLOCKED_SOLVED'
            else: action='UPDATE'
            remote_files=api.get(f"/challenges/{old['id']}/files") if args.upload_files else []
            remote_names={Path(z.get('location','')).name for z in remote_files}
            missing=[p for p in files if p.name not in remote_names]
            if args.upload_files and any(p.name in remote_names for p in files):
                print(f"NOTICE {x['uid']}: существующие имена вложений не перезаписываются (проверь содержимое вручную)")
            entry=(x,action,old['id'],missing,solved)
        else: entry=(x,'CREATE',None,files,0)
        plan.append(entry)
    counts={a:sum(1 for e in plan if e[1]==a) for a in ('CREATE','UPDATE','BLOCKED_TYPE_CHANGE','BLOCKED_SOLVED')}
    print('ПЛАН',counts,'; загрузка файлов:',args.upload_files, '; подсказки: НЕ ТРОГАЕМ')
    for x,act,cid,files,solves in plan:
        print(f"{act:19} {x['uid']:15} id={str(cid):4} баллы={x['points']} приложений={len(files)} solves={solves}")
        if args.upload_files and x['token'] not in ('WEB',) and not files:
            print('  NOTE: отсутствуют файлы для загрузки либо все уже привязаны; проверь путь --root')
    report=Path.cwd()/'import_plan.json'
    report.write_text(json.dumps([{'id':x['uid'],'action':act,'existing_id':cid,'files':[str(p) for p in files],'solves':solves} for x,act,cid,files,solves in plan],ensure_ascii=False,indent=2),encoding='utf-8')
    print('План:',report)
    if not args.apply:
        print('DRY RUN — сервер не изменён. Для импорта используй --apply; рекомендуется сначала создать бэкап CTFd.')
        return
    if counts['BLOCKED_TYPE_CHANGE'] or counts['BLOCKED_SOLVED']:
        sys.exit('Обнаружены блокировки. Импорт отменён целиком; исправь несовместимые задания вручную либо используй --allow-update-solved после бэкапа.')
    confirm=input(f"Будет изменено {counts['UPDATE']} и создано {counts['CREATE']} заданий. Введите IMPORT 50: ")
    if confirm!='IMPORT 50':sys.exit('Отменено')
    for x,act,cid,files,_ in plan:
        initial,decay,minimum=x['points']; base=dict(name=x['name'],category=x['category'],description=x['description'],connection_info=connection(x,args.host),initial=initial,decay=decay,minimum=minimum,function='quadratic',value=initial)
        if act=='CREATE':
            created=api.post('/challenges',json={**base,'type':'dynamic','state':'hidden'}); cid=created['id']
            print(f"CREATED {x['uid']} id={cid} hidden")
        else:
            api.patch(f'/challenges/{cid}',base); print(f"UPDATED {x['uid']} id={cid}")
        flags=api.get(f'/challenges/{cid}/flags')
        if not flags:
            api.post('/flags',json={'challenge_id':cid,'type':'static','content':x['flag'],'data':''}); print('  FLAG created')
        elif len(flags)==1 and flags[0].get('content')==x['flag']:
            print('  FLAG unchanged')
        else:
            print('  FLAG REVIEW: существующий флаг не изменён (чтобы не сломать результаты); сверить вручную')
        if args.upload_files:
            for p in files:
                if not p.exists(): print(f'  MISSING {p}');continue
                with p.open('rb') as fp:
                    api.post('/files',files={'file':(p.name,fp,'application/octet-stream')},data={'challenge_id':str(cid),'type':'challenge'})
                print('  UPLOADED',p.name)
    print('IMPORT FINISHED: подсказки не менялись. Новые задания hidden — проверь и опубликуй вручную.')

if __name__=='__main__':main()
