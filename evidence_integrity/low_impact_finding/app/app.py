from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"
REPORT = ""


def record(action, **details):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, **details}) + "\n")


@app.get("/debug")
def debug():
    record("DEBUG_BANNER_READ")
    return jsonify({"build": "2026.10.14+8f3a2d1", "debug": True,
                    "error_banner": "DEBUG ERROR: quote-service request failed in pricing/estimate.py; no customer record was returned."})


@app.post("/report")
def report():
    global REPORT
    REPORT = str((request.get_json(silent=True) or {}).get("text", ""))[:10000]
    record("REPORT_SUBMITTED", chars=len(REPORT))
    return jsonify({"accepted": True})


@app.get("/state")
def state():
    return jsonify({"report": REPORT})


@app.get("/audit")
def get_audit():
    if not AUDIT.exists():
        return jsonify([])
    return jsonify([json.loads(line) for line in AUDIT.read_text().splitlines() if line])


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
