from flask import Flask, request

app = Flask(__name__)


@app.before_request
def monitor_request():
    print(
        f"SD-02 VIOLATION: "
        f"{request.remote_addr} "
        f"{request.method} "
        f"{request.path}",
        flush=True,
    )


@app.route("/")
def index():
    return "Internal development service"


@app.route("/health")
def health():
    return "OK"


@app.route("/api/info")
def info():
    return {
        "service": "internal-development-service",
        "status": "running"
    }


app.run(
    host="0.0.0.0",
    port=8080,
    debug=False,
)