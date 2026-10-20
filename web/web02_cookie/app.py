from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def index():
 if request.method=='GET':return '<form method=post><input name=login placeholder=Login><input name=password type=password><button>Enter</button></form>'
 if (request.form.get('login'),request.form.get('password'))!=('student','student123'):return 'invalid',403
 r=make_response(redirect('/profile'));r.set_cookie('user_id','1001');return r
@app.route('/profile')
def profile():return 'Student id='+request.cookies.get('user_id','?')+' - try /admin'
@app.route('/admin')
def admin():return ('SPKctf{c00ki3_jar_4dmin}' if request.cookies.get('user_id')=='1' else 'Access denied',200 if request.cookies.get('user_id')=='1' else 403)
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
