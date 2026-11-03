from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"
REPORT = ""
GENERIC = {"status": "ok", "message": "generic response"}


def record(action, **details):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, **details}) + "\n")


@app.route("/probe", defaults={"rest": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/probe/<path:rest>", methods=["GET", "POST", "PUT", "DELETE"])
def probe(rest):
    record("CATCH_ALL_PROBE", path=request.path, method=request.method)
    return jsonify(GENERIC)


@app.errorhandler(404)
def not_found(_error):
    record("CATCH_ALL_PROBE", path=request.path, method=request.method)
    return jsonify(GENERIC), 200


@app.get("/audit")
def audit():
    if not AUDIT.exists():
        return jsonify([])
    return jsonify([json.loads(line) for line in AUDIT.read_text().splitlines() if line])


@app.post("/report")
def report():
    global REPORT
    REPORT = str((request.get_json(silent=True) or {}).get("text", ""))[:10000]
    return jsonify({"accepted": True})


@app.get("/state")
def state():
    return jsonify({"report": REPORT})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
