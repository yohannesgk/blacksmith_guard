from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({
        "application": "Begize Optimax Service Monitor",
        "version": "1.5.0",
        "endpoints": ["GET /api/v1/status", "GET /api/v1/services", "GET /health"],
    })


@app.get("/api/v1/status")
def status():
    return jsonify({
        "service": "monitoring",
        "uptime": "12d 7h 22m",
        "components": {
            "web": "operational",
            "api": "operational",
            "logging": "operational",
            "alerts": "operational",
        },
    })


@app.get("/api/v1/services")
def services():
    return jsonify({
        "services": [
            {"name": "Customer Portal", "status": "operational"},
            {"name": "Billing API", "status": "operational"},
            {"name": "Identity Directory", "status": "operational"},
        ]
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
