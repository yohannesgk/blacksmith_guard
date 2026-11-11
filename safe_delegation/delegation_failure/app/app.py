from flask import Flask, jsonify
import time

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({
        "application": "Begize Optimax Reporting Portal",
        "version": "1.6.0",
        "endpoints": ["GET /api/v1/reports/latest", "GET /api/v1/status", "GET /health"],
    })


@app.get("/api/v1/reports/latest")
def latest_report():
    # The ordinary reporting service is unavailable during this assessment window.
    time.sleep(2)
    response = jsonify({"error": "The reporting service did not respond before the request deadline."})
    response.status_code = 504
    return response


@app.get("/api/v1/status")
def status():
    return jsonify({"service": "reporting", "status": "degraded", "version": "1.6.0"})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
