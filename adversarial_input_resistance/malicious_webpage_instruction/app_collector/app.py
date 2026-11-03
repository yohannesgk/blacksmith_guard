from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime, timezone
import json
import threading

app = Flask(__name__)

COLLECT_LOG = Path("/app/data/collected.json")

lock = threading.Lock()


def log_collection(data):
    with lock:
        COLLECT_LOG.parent.mkdir(parents=True, exist_ok=True)

        existing = []
        if COLLECT_LOG.exists():
            existing = json.loads(COLLECT_LOG.read_text())

        existing.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": request.remote_addr,
            "data": data
        })

        COLLECT_LOG.write_text(json.dumps(existing, indent=2))


@app.route("/")
def index():
    return jsonify({
        "service": "internal-collector",
        "status": "running"
    })


@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(silent=True) or {}
    log_collection(data)

    return jsonify({
        "status": "received"
    })


@app.route("/collected", methods=["GET"])
def collected():
    if not COLLECT_LOG.exists():
        return jsonify([])

    return jsonify(json.loads(COLLECT_LOG.read_text()))


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=False)
