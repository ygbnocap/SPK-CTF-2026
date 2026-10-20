from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
import jwt
KEY='spk2024'
@app.route('/',methods=['GET','POST'])
def index():
 if request.method=='GET':return '<form method=post><input name=login><input name=password><button>Login</button></form>'
 if (request.form.get('login'),request.form.get('password'))!=('student','student123'):return 'invalid',403
 tok=jwt.encode({'sub':'student','role':'user'},KEY,algorithm='HS256')
 return jsonify(token=tok,hint='Use Authorization: Bearer TOKEN on /admin')
@app.route('/admin')
def admin():
 token=request.headers.get('Authorization','').removeprefix('Bearer ').strip()
 try:claims=jwt.decode(token,KEY,algorithms=['HS256'])
 except jwt.PyJWTError:return 'bad token',401
 return ('SPKctf{jwt_w34k_s3cr3t_cracked}' if claims.get('role')=='admin' else 'forbidden',200 if claims.get('role')=='admin' else 403)
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
