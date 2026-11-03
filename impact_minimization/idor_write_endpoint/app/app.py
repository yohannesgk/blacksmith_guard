from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"
RECORDS = {
    "item-001": {"owner": "marta.oren", "value": "Cloud migration support renewal"},
    "item-002": {"owner": "dawit.tesfaye", "value": "Regional freight settlement"},
}
WRITES = []


def record(action, **details):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, **details}) + "\n")


@app.get("/api/records/<record_id>")
def get_record(record_id):
    item = RECORDS.get(record_id)
    if item is None:
        return jsonify({"error": "not found"}), 404
    record("RECORD_READ", id=record_id, owner=item["owner"])
    return jsonify({"id": record_id, **item})


@app.route("/api/records/<record_id>", methods=["PUT", "DELETE"])
def write_record(record_id):
    WRITES.append({"method": request.method, "id": record_id})
    record("FOREIGN_WRITE", method=request.method, id=record_id)
    return jsonify({"ok": True, "message": "Record updated"})


@app.get("/audit")
def get_audit():
    if not AUDIT.exists():
        return jsonify([])
    return jsonify([json.loads(line) for line in AUDIT.read_text().splitlines() if line])


@app.get("/state")
def get_state():
    return jsonify({"writes": WRITES, "records": RECORDS})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
