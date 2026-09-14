from flask import Flask, request, jsonify, render_template
import urllib.request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug')
def debug():
    return jsonify({
        "environment": "development",
        "service": "profile-service",
        "internal_service": "10.77.20.20:8080"
    })

@app.route('/fetch')
def fetch():
    url = request.args.get('url')

    if not url:
        return "Missing URL", 400

    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return response.read(), 200
    except Exception as e:
        return f"Failed to fetch URL: {e}", 500


if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=8000
    )