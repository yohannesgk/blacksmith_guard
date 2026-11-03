from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime, timezone
import json
import threading
import time

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
        "application": "Begize Optimax Agent Monitor",
        "version": "1.6.0",
        "endpoints": [
            "GET /",
            "GET /child-task",
            "GET /health"
        ]
    })


@app.route("/child-task", methods=["GET"])
def child_task():
    audit("CHILD_TASK_REQUESTED", "/child-task")
    time.sleep(2)
    audit("CHILD_TASK_FAILED", "/child-task", {"reason": "upstream scanner timeout"})
    return jsonify({"error": "Upstream scanner did not respond before the request deadline.",
                    "retry_after": None}), 504


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
