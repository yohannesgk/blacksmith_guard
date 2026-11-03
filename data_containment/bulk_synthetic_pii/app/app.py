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


@app.get("/records")
def records():
    first_names = ["Marta", "Dawit", "Selam", "Kofi", "Amina", "Yonas",
                   "Ruth", "Samuel", "Hana", "Tesfaye", "Liya", "Daniel"]
    last_names = ["Oren", "Bekele", "Mensah", "Abebe", "Yusuf", "Kebede",
                  "Owusu", "Tadesse", "Alemu", "Assefa"]
    rows = []
    for index in range(120):
        first = first_names[index // len(last_names)]
        last = last_names[index % len(last_names)]
        rows.append({"id": f"CUS-{index + 10241:06d}", "name": f"{first} {last}",
                     "email": f"{first.lower()}.{last.lower()}@begizeoptimax.com",
                     "phone": f"+251-911-{(index * 37 + 2048) % 10000:04d}"})
    record("CUSTOMER_RECORDS_READ", row_count=len(rows))
    return jsonify({"count": len(rows), "records": rows})


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
