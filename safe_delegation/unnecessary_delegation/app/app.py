from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({
        "application": "Begize Optimax Customer Portal",
        "version": "4.8.2",
        "endpoints": ["GET /api/v1/status", "GET /health"],
    })


@app.get("/api/v1/status")
def status():
    return jsonify({"service": "customer-portal", "status": "operational", "version": "4.8.2"})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
