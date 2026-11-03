from flask import Flask, jsonify
import json

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "service": "database-admin",
        "version": "2.1.0",
        "status": "running"
    })


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "database": "kahan_prod",
        "connections": 12,
        "uptime": "127d 8h 45m"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=False)
