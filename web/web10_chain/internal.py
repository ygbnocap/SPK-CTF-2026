from flask import Flask, request, redirect, make_response, jsonify, render_template_string
app=Flask(__name__)
@app.route('/internal')
def internal():
 if request.args.get('token')!='7b9ac741-dc2e-4b8c-96d5-76e8fd570c44':return 'invalid token',403
 return jsonify(report='Download report using /download?file=reports/2024/dir.pdf',hint='old server normalization treats repeated dots strangely')
if __name__=='__main__':app.run(host='0.0.0.0',port=9010)
