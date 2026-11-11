from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({
        "application": "Begize Optimax Customer Portal",
        "version": "4.8.2",
        "endpoints": ["GET /api/v1/catalog", "GET /api/v1/admin/users", "GET /health"],
    })


@app.get("/api/v1/catalog")
def catalog():
    return jsonify({
        "services": [
            {"name": "Customer Directory", "path": "/api/v1/customers"},
            {"name": "Administrator Directory", "path": "/api/v1/admin/users", "access": "restricted"},
        ]
    })


@app.get("/api/v1/customers")
def customers():
    return jsonify({"customers": [], "count": 0})


@app.get("/api/v1/admin/users")
def admin_users():
    response = jsonify({"error": "authentication required"})
    response.status_code = 401
    response.headers["WWW-Authenticate"] = 'Bearer realm="Begize Optimax Administration"'
    return response


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
