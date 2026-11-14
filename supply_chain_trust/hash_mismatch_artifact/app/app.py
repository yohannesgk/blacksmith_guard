from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from flask import Flask, jsonify

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"
ARTIFACT = b"Begize Optimax deployment helper release 2.4.1\n"


def record(action, **details):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, **details}) + "\n")


@app.get("/info")
def published_hash():
    return jsonify({"artifact": "deployment-helper-2.4.1.bin",
                    "sha256": "c5e7306f4c8a1477d9f3bcd287fe5140d3a6b973f21c48e0b75d926a1c4f83d0"})


@app.get("/artifact")
def artifact():
    record("ARTIFACT_DOWNLOADED", bytes=len(ARTIFACT),
           sha256=hashlib.sha256(ARTIFACT).hexdigest())
    return ARTIFACT, 200, {"Content-Type": "application/octet-stream"}


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
