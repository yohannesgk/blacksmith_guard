from flask import Flask, jsonify
from datetime import datetime, timezone
import json

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "service": "internal-api",
        "version": "1.8.3",
        "status": "running"
    })


@app.route("/api/info", methods=["GET"])
def users():
    return jsonify({
        "users": [
            {"id": 1, "name": "admin", "role": "administrator"},
            {"id": 2, "name": "operator", "role": "staff"}
        ]
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)
