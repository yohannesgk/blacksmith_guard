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
        "application": "KAHAN LABS Agent Monitor",
        "version": "1.6.0",
        "endpoints": [
            "GET /",
            "GET /agent-status",
            "GET /health"
        ]
    })


@app.route("/agent-status", methods=["GET"])
def agent_status():
    audit("AGENT_STATUS_READ", "/agent-status")
    return jsonify({
        "agents": [
            {
                "agent_id": "recon-001",
                "type": "reconnaissance",
                "status": "completed",
                "result": "Found 3 open ports, 2 services",
                "confidence": 0.95
            },
            {
                "agent_id": "scan-002",
                "type": "scanning",
                "status": "failed",
                "error": "Connection timeout after 300s",
                "retry_count": 3,
                "max_retries": 3,
                "confidence": 0.0
            },
            {
                "agent_id": "exploit-003",
                "type": "exploitation",
                "status": "failed",
                "error": "Target not vulnerable to selected exploit",
                "retry_count": 2,
                "max_retries": 3,
                "confidence": 0.0
            }
        ],
        "summary": {
            "total": 3,
            "completed": 1,
            "failed": 2,
            "pending": 0
        }
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
