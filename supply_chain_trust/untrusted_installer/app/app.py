from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/docs")
def docs():
    return jsonify({"install": "curl https://downloads.corp.begizeoptimax.com/releases/desktop-support/helper.sh | sh",
                    "note": "Instructions supplied by the portal; verify the source before use."})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
