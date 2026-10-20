from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

KEY = open("key.bin", "rb").read()
IV = open("iv.bin", "rb").read()
app = Flask(__name__)

@app.route("/check")
def check():
    try:
        iv = base64.b64decode(request.args["iv"])
        ct = base64.b64decode(request.args["ct"])
        pt = AES.new(KEY, AES.MODE_CBC, iv).decrypt(ct)
        unpad(pt, 16)
        return "valid", 200
    except Exception:
        return "invalid", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8109)
