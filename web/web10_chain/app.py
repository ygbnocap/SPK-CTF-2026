from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
import requests,uuid,os
TOKEN='7b9ac741-dc2e-4b8c-96d5-76e8fd570c44'
@app.route('/')
def home():return '<h1>SPK Notes Portal</h1><p>Login user / user123 via /login; /notes?id=1001, /fetch?url=, /download?file=</p>'
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='GET':return '<form method=post><input name=login><input name=password><button>Login</button></form>'
 if (request.form.get('login'),request.form.get('password'))!=('user','user123'):return 'wrong',403
 r=make_response(redirect('/notes?id=1001'));r.set_cookie('session','user');return r
def authorized():return request.cookies.get('session')=='user'
@app.route('/notes')
def notes():
 if not authorized():return 'login required',401
 uid=request.args.get('id','1001')
 if uid=='1':return jsonify(id=1,owner='director',note='internal report API bearer token: '+TOKEN)
 if uid=='1001':return jsonify(id=1001,owner='user',note='Welcome to Notes')
 return 'not found',404
@app.route('/fetch')
def fetch():
 if not authorized():return 'login required',401
 url=request.args.get('url','')
 if not url.startswith(('http://','https://')):return 'invalid URL',400
 if '127.0.0.1' in url or 'localhost' in url:return 'blocked',403
 try:return requests.get(url,timeout=3,allow_redirects=False).text
 except requests.RequestException:return 'unreachable',502
@app.route('/download')
def download():
 if not authorized():return 'login required',401
 name=request.args.get('file','')
 # deliberately unsafe normalization; ....// bypasses simple ../ removal
 name=name.replace('../','')
 path=os.path.normpath('/app/files/'+name)
 try:
  with open(path,'rb') as f:return f.read(),200,{'Content-Type':'application/octet-stream'}
 except OSError:return 'not found',404
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
