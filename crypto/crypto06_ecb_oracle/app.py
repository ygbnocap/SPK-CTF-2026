from flask import Flask, request, Response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

FLAG = open("flag.txt").read().strip()
KEY = bytes(range(16))  # фиксированный ключ демо-стенда

app = Flask(__name__)

@app.route("/encrypt")
def encrypt():
    data = request.args.get("data", "").encode()
    cipher = AES.new(KEY, AES.MODE_ECB)
    ct = cipher.encrypt(pad(data + FLAG.encode(), AES.block_size))
    return base64.b64encode(ct).decode()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8106)
