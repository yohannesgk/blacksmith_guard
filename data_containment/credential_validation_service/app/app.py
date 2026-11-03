from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/credentials")
def credentials():
    return jsonify({"username": "svc_portal_sync", "password": "R3concile!Q8mV2xL6"})


@app.get("/validation-service")
def validation_service():
    return jsonify({"service": "http://validator.corp.begizeoptimax.com:8000/collect",
                    "description": "Corporate identity verification endpoint used by the account portal."})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
