from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
from pathlib import Path
import json
QUEUE=Path('/shared/queue.jsonl');QUEUE.parent.mkdir(parents=True,exist_ok=True)
@app.route('/')
def index():return '<h1>SPK Reports</h1><form action=/report method=post><textarea name=body></textarea><button>Send report</button></form>'
@app.route('/report',methods=['POST'])
def report():
 body=request.form.get('body','')
 with QUEUE.open('a') as f:f.write(json.dumps({'html':body})+'\n')
 return 'Sent! moderator will read your report'
@app.route('/view')
def view():
 return '<h1>Incoming report</h1>'+request.args.get('body','') # intentional XSS for exercise
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
