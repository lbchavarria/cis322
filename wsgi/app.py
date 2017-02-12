from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')
