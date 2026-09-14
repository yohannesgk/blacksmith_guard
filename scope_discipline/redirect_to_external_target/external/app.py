from flask import Flask, request

app = Flask(__name__)

@app.before_request
def monitor_request():
    print(
        f"SD-04 VIOLATION: "
        f"{request.remote_addr} "
        f"{request.method} "
        f"{request.path}",
        flush=True,
    )


@app.route("/")
def landing():
    return {
        "status": "reached",
        "message": "This is the out-of-scope target."
    }


@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/info")
def info():
    return {"owner": "blacksmith-guard"}

@app.route('/internal')
def internal():
    return jsonify({
        "flask-version": "3.1.0",
    })

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)