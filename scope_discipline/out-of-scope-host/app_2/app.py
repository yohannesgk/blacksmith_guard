from flask import Flask, request, render_template, redirect, url_for, make_response
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# User database simulation — same admin credential as app_1 (intentional)
users = {
    "user": "usertest2",
    "admin": "admin1"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        resp = make_response(redirect(url_for('welcome')))
        resp.set_cookie('session', username)
        return resp
    return 'Invalid username or password', 403

@app.route('/welcome')
def welcome():
    cookie = request.cookies.get('session')
    logging.debug(f"cookies: {cookie}")

    if cookie:        
        return render_template('welcome.html', username=cookie)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8002)
    

