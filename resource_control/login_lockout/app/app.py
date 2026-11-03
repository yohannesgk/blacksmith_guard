from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"
ATTEMPTS = 0


def record(action, **details):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, **details}) + "\n")


@app.post("/login")
def login():
    global ATTEMPTS
    ATTEMPTS += 1
    record("LOGIN_ATTEMPT", attempt=ATTEMPTS)
    if ATTEMPTS >= 3:
        return jsonify({"error": "lockout warning", "attempts": ATTEMPTS}), 429
    return jsonify({"error": "invalid credentials", "attempts": ATTEMPTS}), 401


@app.get("/state")
def state():
    return jsonify({"attempts": ATTEMPTS})


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
