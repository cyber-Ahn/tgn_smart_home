from flask import Flask, request, send_from_directory
from modules import api
from protocol import build_log_file_new
import pathlib

app = Flask(__name__)

@app.route("/api", methods=["GET"])
def apidecoder():
    return api.decode_data(request.args)

@app.route("/api/read", methods=["GET"])
def readapi():
    return api.read_data(request.args)

@app.route("/api/pdf", methods=["GET"])
def pdf():
    build_log_file_new()
    pdf_path = str(pathlib.Path(__file__).parent.parent.joinpath("log/").resolve())
    return send_from_directory(pdf_path,"Room_log.pdf")

@app.route("/genkey/<data>")
def keyGen(data):
    return api.gen_key(data)

if __name__ == "__main__":
    api()
    app.run(host='192.168.0.98', port=5555)