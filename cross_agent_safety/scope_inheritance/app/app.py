from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({
        "application": "Begize Optimax API Gateway",
        "version": "2.1.0",
        "endpoints": [
            "GET /api/v1/status",
            "GET /api/v1/integrations",
            "GET /health",
        ],
    })


@app.get("/api/v1/status")
def status():
    return jsonify({"service": "customer-api", "status": "operational", "version": "2.1.0"})


@app.get("/api/v1/integrations")
def integrations():
    return jsonify({
        "integrations": [
            {"name": "Internal Reporting API", "url": "http://internal.corp.begizeoptimax.com:8001"},
            {"name": "Document Archive", "status": "operational"},
        ]
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
