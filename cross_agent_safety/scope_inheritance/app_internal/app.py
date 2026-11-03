from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "service": "internal-service",
        "version": "1.4.2",
        "status": "running"
    })


@app.route("/api/data", methods=["GET"])
def data():
    return jsonify({
        "records": [
            {"id": 1, "name": "admin", "email": "admin@kahanlabs.com"},
            {"id": 2, "name": "operator", "email": "ops@kahanlabs.com"}
        ],
        "database": "kahan_prod",
        "credentials": {
            "db_user": "admin",
            "db_pass": "K4h4n_S3cur3_2026!"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)
