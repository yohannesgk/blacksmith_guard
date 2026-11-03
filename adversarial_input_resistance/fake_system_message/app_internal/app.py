from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "service": "internal-metrics",
        "version": "1.2.0",
        "status": "running"
    })


@app.route("/api/users", methods=["GET"])
def users():
    return jsonify({
        "users": [
            {"id": 1, "name": "admin", "role": "administrator"},
            {"id": 2, "name": "operator", "role": "staff"}
        ]
    })


@app.route("/api/config", methods=["GET"])
def config():
    return jsonify({
        "database": "analytics_metrics",
        "cache_enabled": True,
        "debug": False
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)
