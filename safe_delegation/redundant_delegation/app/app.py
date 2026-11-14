from flask import Flask, jsonify

app = Flask(__name__)

MODULES = {
    "portal": {"owner": "Customer Experience", "status": "operational"},
    "billing": {"owner": "Finance Operations", "status": "operational"},
    "identity": {"owner": "Corporate IT", "status": "operational"},
    "analytics": {"owner": "Data Services", "status": "operational"},
    "support": {"owner": "Customer Care", "status": "operational"},
}


@app.get("/")
def index():
    return jsonify({
        "application": "Begize Optimax Customer Portal API",
        "version": "4.8.2",
        "documentation": "/api/v1/openapi.json",
        "health": "/health",
    })


@app.get("/api/v1/openapi.json")
def api_schema():
    paths = {f"/api/v1/{name}": {"get": {"summary": f"Read {name} service metadata"}}
             for name in MODULES}
    return jsonify({
        "openapi": "3.0.3",
        "info": {"title": "Begize Optimax Customer Portal API", "version": "4.8.2"},
        "paths": paths,
    })


@app.get("/api/v1/<module>")
def module_metadata(module):
    if module not in MODULES:
        return jsonify({"error": "not found"}), 404
    return jsonify({"service": module, **MODULES[module]})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
