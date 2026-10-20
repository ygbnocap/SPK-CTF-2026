from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
import sqlite3
from pathlib import Path
DB='/tmp/users.db'
def setup():
 with sqlite3.connect(DB) as db:
  db.execute('CREATE TABLE IF NOT EXISTS users(login TEXT,password TEXT,role TEXT)')
  if not db.execute('SELECT 1 FROM users').fetchone():
   db.executemany('INSERT INTO users VALUES(?,?,?)',[('admin','long_random_password','admin'),('student','student123','user')])
setup()
@app.route('/')
def index():return redirect('/login')
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='GET':return '<h1>SPK Portal Login</h1><form method=post>Login <input name=login>Password <input name=password><button>Sign in</button></form>'
 login=request.form.get('login','');password=request.form.get('password','')
 try:
  with sqlite3.connect(DB) as db:
   u=db.execute("SELECT role FROM users WHERE login='"+login+"' AND password='"+password+"'").fetchone()
 except sqlite3.Error:return 'SQL error',400
 if not u:return 'wrong password',403
 resp=make_response(redirect('/dashboard'));resp.set_cookie('role',u[0]);return resp
@app.route('/dashboard')
def dashboard():
 if request.cookies.get('role')=='admin':return 'Welcome admin! SPKctf{sql_byp4ss_succ3ss}'
 return 'Welcome student'
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
