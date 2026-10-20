from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
import requests
@app.route('/')
def index():return '<form action=/fetch>URL: <input name=url><button>Fetch</button></form>'
@app.route('/fetch')
def fetch():
 url=request.args.get('url','');
 if not url.startswith(('http://','https://')):return 'HTTP URLs only',400
 if '127.0.0.1' in url.lower() or 'localhost' in url.lower():return 'blocked',403
 try:return requests.get(url,timeout=3,allow_redirects=False).text
 except requests.RequestException:return 'unreachable',502
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
