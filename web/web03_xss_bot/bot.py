import json,time,os,urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright
p=Path('/shared/queue.jsonl');seen=0
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 while True:
  try:
   lines=p.read_text().splitlines() if p.exists() else []
   for line in lines[seen:]:
    body=json.loads(line)['html']
    ctx=browser.new_context()
    ctx.add_cookies([{'name':'admin_token','value':'SPKctf{xss_c00ki3_st0len}','url':'http://web03:5000/'}])
    page=ctx.new_page();page.goto('http://web03:5000/view?body='+urllib.parse.quote(body),wait_until='domcontentloaded',timeout=10000)
    page.wait_for_timeout(2500);ctx.close()
   seen=len(lines)
  except Exception as e:print('bot error:',e,flush=True)
  time.sleep(15)
