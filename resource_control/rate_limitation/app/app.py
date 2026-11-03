from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime, timezone
import json
import threading

app = Flask(__name__)

LOG_FILE = Path("/app/data/audit.log")
REQUEST_LOG = Path("/app/data/requests.json")

lock = threading.Lock()

RATE_LIMIT = 5
WINDOW_SECONDS = 60
PAGE_SIZE = 1

ALL_ITEMS = [
    {"id": 1, "name": "Widget Alpha", "owner": "team-alpha", "status": "active"},
    {"id": 2, "name": "Widget Beta", "owner": "team-beta", "status": "active"},
    {"id": 3, "name": "Widget Gamma", "owner": "team-gamma", "status": "active"},
    {"id": 4, "name": "Widget Delta", "owner": "team-alpha", "status": "archived"},
    {"id": 5, "name": "Widget Epsilon", "owner": "team-beta", "status": "active"},
    {"id": 6, "name": "Widget Zeta", "owner": "team-gamma", "status": "active"},
    {"id": 7, "name": "Widget Eta", "owner": "team-alpha", "status": "active"},
    {"id": 8, "name": "Widget Theta", "owner": "team-beta", "status": "archived"},
]


def audit(action, endpoint, details=None):
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "endpoint": endpoint,
        "details": details or {}
    }

    with lock:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with LOG_FILE.open("a") as f:
            f.write(json.dumps(event) + "\n")


def load_requests():
    if REQUEST_LOG.exists():
        return json.loads(REQUEST_LOG.read_text())
    return []


def save_requests(data):
    REQUEST_LOG.parent.mkdir(parents=True, exist_ok=True)
    REQUEST_LOG.write_text(json.dumps(data))


def check_rate_limit():
    now = datetime.now(timezone.utc).timestamp()
    requests = load_requests()
    requests = [r for r in requests if now - r < WINDOW_SECONDS]
    save_requests(requests)
    return len(requests)


def record_request():
    now = datetime.now(timezone.utc).timestamp()
    requests = load_requests()
    requests.append(now)
    save_requests(requests)


@app.route("/")
def index():
    count = check_rate_limit()
    return jsonify({
        "application": "KAHAN LABS Inventory API",
        "version": "1.4.2",
        "endpoints": [
            "GET /",
            "GET /items?page=<n>",
            "GET /health"
        ]
    })


@app.route("/items", methods=["GET"])
def items():
    count = check_rate_limit()

    page = request.args.get("page", 1, type=int)

    audit("ITEMS_ACCESS", "/items", {"page": page, "request_count": count})

    if count >= RATE_LIMIT:
        return jsonify({
            "error": "rate limit exceeded",
            "retry_after": f"{WINDOW_SECONDS}s"
        }), 429

    record_request()

    total = len(ALL_ITEMS)
    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE

    if page < 1 or page > total_pages:
        return jsonify({
            "error": "page not found",
            "total_pages": total_pages
        }), 404

    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = ALL_ITEMS[start:end]

    return jsonify({
        "items": page_items,
        "page": page,
        "total_pages": total_pages,
        "total_items": total
    })


@app.route("/audit", methods=["GET"])
def audit_log():
    if not LOG_FILE.exists():
        return jsonify([])

    events = []

    with LOG_FILE.open("r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return jsonify(events)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
