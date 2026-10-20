from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
@app.route('/')
def index():return redirect('/login')
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='GET':return '<form method=post>Login<input name=login>Password<input name=password><button>Go</button></form>'
 if (request.form.get('login'),request.form.get('password'))!=('student','student123'):return 'wrong',403
 r=make_response(redirect('/profile?id=1001'));r.set_cookie('session','student');return r
@app.route('/profile')
def profile():
 if request.cookies.get('session')!='student':return 'login required',401
 user_id=request.args.get('id','1001')
 if user_id=='1':return jsonify(id=1,name='Director',notes='SPKctf{id0r_v3rtic4l_priv4sc}')
 if user_id=='1001':return jsonify(id=1001,name='Student',notes='Just a regular user')
 return 'not found',404
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
