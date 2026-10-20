from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
@app.route('/flag')
def flag():return 'SPKctf{ssrf_internal_access}'
if __name__=='__main__':app.run(host='0.0.0.0',port=9000)
