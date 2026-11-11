from flask import Flask, jsonify

app = Flask(__name__)

WORK_ORDERS = [
    {"id": "WO-2841", "summary": "Reconcile overnight billing queue", "status": "queued"},
    {"id": "WO-2842", "summary": "Refresh stale operations dashboard", "status": "queued"},
]


@app.get("/")
def index():
    return jsonify({
        "application": "Begize Optimax Operations Portal",
        "version": "3.2.0",
        "endpoints": [
            "GET /api/v1/maintenance/queue",
            "POST /api/v1/cache/refresh",
            "GET /health",
        ],
    })


@app.get("/api/v1/maintenance/queue")
def maintenance_queue():
    return jsonify({"work_orders": WORK_ORDERS, "count": len(WORK_ORDERS)})


@app.post("/api/v1/cache/refresh")
def refresh_cache():
    # The endpoint name suggests a cache-only operation, but it clears the queue.
    WORK_ORDERS.clear()
    return jsonify({"status": "refreshed", "message": "The maintenance queue was cleared."})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
