from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
import sqlite3
DB='/tmp/search.db'
with sqlite3.connect(DB) as db:
 db.execute('CREATE TABLE IF NOT EXISTS items(name TEXT)');db.execute('CREATE TABLE IF NOT EXISTS secret(flag TEXT)')
 if not db.execute('SELECT 1 FROM items').fetchone():db.execute("INSERT INTO items VALUES('test')")
 if not db.execute('SELECT 1 FROM secret').fetchone():db.execute("INSERT INTO secret VALUES('SPKctf{blind_sql_3xtr4ction}')")
@app.route('/')
def home():return '<form action=/search><input name=q><button>Search</button></form>'
@app.route('/search')
def search():
 q=request.args.get('q','')
 try:
  with sqlite3.connect(DB) as db:found=db.execute("SELECT 1 FROM items WHERE name='"+q+"' LIMIT 1").fetchone()
 except sqlite3.Error:return 'пусто'
 return 'найдено' if found else 'пусто'
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
