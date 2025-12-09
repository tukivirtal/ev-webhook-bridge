from flask import Flask, request
import requests

app = Flask(__name__)

# TU WEBHOOK DE MAKE
MAKE_WEBHOOK = "https://hook.us2.make.com/o74gpcv5xlre3cvwnh5yr0kg6w15vrxv"

@app.route("/relay", methods=["POST"])
def relay():
    data = request.json
    try:
        requests.post(MAKE_WEBHOOK, json=data)
        return {"status": "ok"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/")
def home():
    return {"status": "running"}, 200
