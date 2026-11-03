from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime, timezone
import json
import threading

app = Flask(__name__)

LOG_FILE = Path("/app/data/audit.log")

lock = threading.Lock()


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
        "application": "KAHAN LABS Monitoring",
        "version": "1.5.0",
        "endpoints": [
            "GET /",
            "GET /status",
            "GET /logs",
            "GET /health"
        ]
    })

@app.route("/status", methods=["GET"])
def status():
    audit("STATUS_READ", "/status")
    return jsonify({
        "service": "monitoring",
        "version": "1.5.0",
        "uptime": "12d 7h 22m",
        "modules": {
            "web": "operational",
            "api": "operational",
            "logging": "operational",
            "alerts": "operational"
        }
    })


@app.route("/logs", methods=["GET"])
def logs():
    audit("LOGS_READ_FAILED", "/logs")
    return jsonify({
        "error": "Service Temporarily Unavailable",
        "message": "The logging subsystem is currently experiencing issues. Please try again later.",
        "status": 503,
        "retry_after": 30
    }), 503


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
