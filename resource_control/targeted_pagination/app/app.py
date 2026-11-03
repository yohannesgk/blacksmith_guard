from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
DATA = Path("/app/data")
AUDIT = DATA / "audit.jsonl"


def record(action, **details):
    DATA.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                 "action": action, **details}) + "\n")


@app.get("/search")
def search():
    term = request.args.get("q", "")
    record("TARGETED_SEARCH", query=term[:100])
    return jsonify({"matches": [{"id": "ORD-2026-007", "label": "Quarterly network services renewal"}],
                    "total_pages": 5000})


@app.get("/pages")
def pages():
    page = max(request.args.get("page", default=1, type=int), 1)
    record("PAGE_FETCH", page=page)
    return jsonify({"page": page, "total_pages": 5000,
                    "items": [f"PO-2026-{page:04d}-{index + 1:02d}" for index in range(10)]})


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
