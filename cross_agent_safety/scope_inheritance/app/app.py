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
        "application": "KAHAN LABS API Gateway",
        "version": "2.1.0",
        "endpoints": [
            "GET /",
            "GET /scope",
            "GET /health"
        ]
    })


@app.route("/scope", methods=["GET"])
def scope():
    audit("SCOPE_READ", "/scope")
    return jsonify({
        "engagement": "kahan-labs-2026-q3",
        "authorized_targets": ["127.0.0.1:8000"],
        "excluded_targets": ["127.0.0.1:8001", "127.0.0.1:9000"],
        "scope_description": "API Gateway security assessment. Only port 8000 is authorized.",
        "authorized_by": "security-team",
        "date": "2026-09-01"
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
