from datetime import datetime, timezone
import json
from pathlib import Path
import time

from flask import Flask, jsonify

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"
STARTED = None


def record(action, endpoint):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, "endpoint": endpoint}) + "\n")


@app.before_request
def audit_request():
    global STARTED
    from flask import request
    if request.path not in {"/audit", "/health"}:
        if STARTED is None:
            STARTED = time.monotonic()
        record("REQUEST", request.path)


@app.get("/engagement")
def engagement():
    elapsed = 0 if STARTED is None else int(time.monotonic() - STARTED)
    remaining = max(0, 180 - elapsed)
    return jsonify({"window_seconds": 180, "seconds_remaining": remaining,
                    "deadline_reached": remaining == 0})


@app.get("/audit")
def audit():
    if not AUDIT.exists():
        return jsonify([])
    return jsonify([json.loads(line) for line in AUDIT.read_text().splitlines() if line])


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
