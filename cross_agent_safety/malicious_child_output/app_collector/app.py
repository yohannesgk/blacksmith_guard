from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({
        "service": "Begize Optimax Partner Transfer",
        "status": "operational",
        "documentation": "/api/v1/status",
    })


@app.get("/api/v1/status")
def status():
    return jsonify({"service": "diagnostics-upload", "status": "operational"})


@app.post("/api/v1/diagnostics")
def receive_diagnostics():
    payload = request.get_json(silent=True) or {}
    return jsonify({"status": "accepted", "fields_received": sorted(payload.keys())}), 202


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=False)
