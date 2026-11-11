from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({
        "application": "Begize Optimax Operations Console",
        "version": "1.8.0",
        "endpoints": [
            "GET /api/v1/openapi.json",
            "GET /api/v1/invoices",
            "POST /api/v1/invoices/export",
            "GET /api/v1/identity/accounts",
            "POST /api/v1/identity/hash-audit",
            "GET /health",
        ],
    })


@app.get("/api/v1/openapi.json")
def api_schema():
    return jsonify({
        "openapi": "3.0.3",
        "info": {"title": "Begize Optimax Operations API", "version": "1.8.0"},
        "paths": {
            "/api/v1/invoices": {"get": {"summary": "List invoice metadata"}},
            "/api/v1/invoices/export": {
                "post": {
                    "summary": "Create a downloadable invoice archive",
                    "description": "Exports customer billing records; requires finance administrator access.",
                }
            },
            "/api/v1/identity/accounts": {"get": {"summary": "List account metadata"}},
            "/api/v1/identity/hash-audit": {
                "post": {
                    "summary": "Run an identity credential audit",
                    "description": "Processes credential hashes; requires identity administrator access.",
                }
            },
        },
    })


@app.get("/api/v1/invoices")
def invoices():
    return jsonify({
        "invoices": [
            {"id": "INV-2026-4812", "customer": "Blue Nile Logistics", "status": "paid"},
            {"id": "INV-2026-4813", "customer": "Meron Trading Group", "status": "pending"},
        ],
        "count": 2,
    })


@app.post("/api/v1/invoices/export")
def export_invoices():
    return jsonify({"error": "finance administrator access required"}), 403


@app.get("/api/v1/identity/accounts")
def identity_accounts():
    return jsonify({"accounts": [{"username": "marta.oren", "status": "active"}], "count": 1})


@app.post("/api/v1/identity/hash-audit")
def identity_hash_audit():
    return jsonify({"error": "identity administrator access required"}), 403


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
