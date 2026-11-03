from flask import Flask, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("http://billing.corp.begizeoptimax.com:8002/", code=302)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
