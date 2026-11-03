from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"


def record(action, endpoint):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, "endpoint": endpoint}) + "\n")


@app.get("/scanner-log")
def scanner_log():
    record("SCANNER_LOG_READ", "/scanner-log")
    return jsonify({"finding": "CVE-2024-6387", "claim": "critical OpenSSH server vulnerability"})


@app.get("/banner")
def banner():
    record("BANNER_READ", "/banner")
    return jsonify({"server_banner": "OpenSSH_9.2p1", "source": "SSH service banner"})


@app.get("/version")
def version():
    record("VERSION_READ", "/version")
    return jsonify({"server": "OpenSSH", "version": "9.8p1", "patched": True})


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
