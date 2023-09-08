from flask import Flask, request
from modules import api

app = Flask(__name__)

@app.route("/api", methods=["GET"])
def apidecoder():
    return api.decode_data(request.args)

@app.route("/api/read", methods=["GET"])
def readapi():
    return api.read_data(request.args)

@app.route("/genkey/<data>")
def keyGen(data):
    return api.gen_key(data)

if __name__ == "__main__":
    api()
    app.run(host='192.168.0.98', port=5555)