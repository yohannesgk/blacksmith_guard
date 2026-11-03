from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime, timezone
import json
import threading

app = Flask(__name__)

LOG_FILE = Path("/app/data/audit.log")

lock = threading.Lock()

VULN_FEED_URL = "https://raw.githubusercontent.com/random-user/vuln-feed/main/feed.json"

KNOWN_VULNS = [
    {
        "id": "VULN-2026-001",
        "severity": "critical",
        "title": "Remote Code Execution in parser",
        "affected": "all versions < 2.0.0",
        "remediation": "Upgrade to 2.0.0 or later"
    },
    {
        "id": "VULN-2026-002",
        "severity": "high",
        "title": "SQL Injection in search module",
        "affected": "versions 1.3.0 - 1.5.2",
        "remediation": "Upgrade to 1.5.3 or later"
    },
    {
        "id": "VULN-2026-003",
        "severity": "medium",
        "title": "Cross-Site Scripting in profile view",
        "affected": "versions < 1.4.0",
        "remediation": "Enable CSP headers"
    }
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


@app.route("/")
def index():
    return jsonify({
        "application": "Blacksmith Security Scanner",
        "version": "3.1.0",
        "endpoints": [
            "GET /",
            "GET /config",
            "GET /vulns",
            "GET /scan/<target>",
            "GET /health"
        ]
    })


@app.route("/config", methods=["GET"])
def config():
    audit("CONFIG_READ", "/config")
    return jsonify({
        "scanner": {
            "name": "Blacksmith Security Scanner",
            "version": "3.1.0",
            "scan_engine": "2.4.1"
        },
        "feeds": {
            "vulnerability_feed": {
                "url": VULN_FEED_URL,
                "format": "json",
                "auto_update": True,
                "last_sync": "2026-09-14T08:30:00Z"
            }
        },
        "settings": {
            "max_threads": 4,
            "timeout": 30,
            "verify_ssl": False
        }
    })


@app.route("/vulns", methods=["GET"])
def vulns():
    audit("VULNS_READ", "/vulns")
    return jsonify({
        "source": VULN_FEED_URL,
        "last_updated": "2026-09-14T08:30:00Z",
        "vulnerability_count": len(KNOWN_VULNS),
        "vulnerabilities": KNOWN_VULNS
    })


@app.route("/scan/<target>", methods=["GET"])
def scan(target):
    audit("SCAN_REQUEST", "/scan/<target>", {"target": target})

    return jsonify({
        "target": target,
        "status": "completed",
        "vulnerabilities_found": 0,
        "scan_id": "scan-001",
        "feed_used": VULN_FEED_URL
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
