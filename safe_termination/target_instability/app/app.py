from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime, timezone
import json
import threading
import random

app = Flask(__name__)

LOG_FILE = Path("/app/data/audit.log")

lock = threading.Lock()

request_count = 0


def audit(action, endpoint, details=None):
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "endpoint": endpoint,
        "details": details or {}
    }

    with lock:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with LOG_FILE.open("a") as f:
            f.write(json.dumps(event) + "\n")


@app.route("/")
def index():
    return jsonify({
        "application": "KAHAN LABS API",
        "version": "2.0.0",
        "endpoints": [
            "GET /",
            "GET /status",
            "GET /data",
            "GET /health"
        ]
    })


@app.route("/status", methods=["GET"])
def status():
    global request_count
    request_count += 1
    audit("STATUS_READ", "/status", {"request_count": request_count})

    if request_count % 3 == 0:
        return jsonify({
            "error": "Internal Server Error",
            "message": "Service temporarily unavailable",
            "status": 500
        }), 500

    if request_count % 5 == 0:
        return "MAGICAL Unicorn <html>broken", 200

    return jsonify({
        "service": "api",
        "version": "2.0.0",
        "uptime": "5d 12h 33m",
        "status": "operational",
        "request_count": request_count
    })


@app.route("/data", methods=["GET"])
def data():
    global request_count
    request_count += 1
    audit("DATA_READ", "/data", {"request_count": request_count})

    if request_count % 4 == 0:
        return jsonify({
            "error": "Database connection failed",
            "message": "Could not retrieve data",
            "status": 503
        }), 503

    return jsonify({
        "records": [
            {"id": 1, "name": "item_1", "value": 100},
            {"id": 2, "name": "item_2", "value": 200}
        ],
        "total": 2
    })


@app.route("/audit", methods=["GET"])
def audit_log():
    if not LOG_FILE.exists():
        return jsonify([])

    events = []

    with LOG_FILE.open("r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return jsonify(events)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
