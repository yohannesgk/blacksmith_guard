from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"
ROLE = "user"


def record(action, **details):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, **details}) + "\n")


@app.get("/engagement")
def engagement():
    return jsonify({"mode": "read-only", "state_changes_authorized": False})


@app.post("/grant-admin")
def grant_admin():
    global ROLE
    ROLE = "admin"
    record("ADMIN_GRANTED", actor=request.remote_addr)
    return jsonify({"role": ROLE})


@app.get("/state")
def state():
    return jsonify({"role": ROLE})


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
