from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
@app.route('/')
def index():return 'Say hello at /hello?name=...'
@app.route('/hello')
def hello():return render_template_string('Hello, '+request.args.get('name','guest')+'!')
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
