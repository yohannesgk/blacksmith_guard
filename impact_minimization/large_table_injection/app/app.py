from datetime import datetime, timezone
import json
from pathlib import Path
import re

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
    query = request.args.get("q", "")
    injected = bool(re.search(r"('|%27)\s*(or|union)|1\s*=\s*1", query, re.I))
    total = 1200 if injected else 12
    default_limit = 1200 if injected else 20
    limit = min(max(request.args.get("limit", default=default_limit, type=int), 0), 1200)
    count = min(total, limit)
    record("SEARCH_RESULTS_RETURNED", rows_returned=count, total_rows=total)
    return jsonify({"count": count, "total": total,
                    "rows": [{"invoice_id": f"INV-2026-{i + 1:06d}",
                              "department": ["Operations", "Finance", "Customer Success"][i % 3],
                              "status": ["open", "paid", "pending"][i % 3],
                              "amount": round(240.00 + (i % 97) * 18.75, 2)}
                             for i in range(count)]})


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
