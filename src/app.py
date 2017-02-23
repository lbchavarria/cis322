from flask import Flask, render_template, request
from config import dbname, dbhost, dbport
import json
import psycopg2

app = Flask(__name__)

@app.route('/create_user',methods=('GET','POST'))
def create_user():

    if request.method=='GET':
        return render_template('create_user.html')
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            with psycopg2.connect(name=dbname,host=dbhost,port=dbport) as connect:
                cur = connect.cursor()
                sql = "SELECT COUNT(*) FROM users WHERE username=%s"
                cur.execute(sql,(username,))
                res = cur.fetchone()[0]
                if res != 0:
                    session['error'] = 'The username %s is already taken'%username
                    return redirect('error')
                sql = "INSERT INTO users (username.password) VALUES (%s,%s)"
                cur.execute(sql,(username,password))
                session['success'] = 'The username %s has been added'%username
                return redirect('success')
            session['error'] = 'Invalid form fields'
            return redirect('error')
        session['error'] = 'Invalid HTTP method %s'%request.method
        return redirect('error')


@app.route('/login',methods=('GET','POST'))
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            with psycopg2.connect(name=dbname,host=dbhost,port=dbport) as connect:
                cur = connect.cursor()
                sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
                cur.execute(sql,(username,password))
                res = cur.fetchone()[0]
                if res != 1:
                    session['error'] = 'Authentication failed'
                    return redirect('error')
                session['username']=username
                return redirect('dashboard')
            session['error'] = 'Invalid form fields'
            return redirect('error')
        session['error'] = 'Invalid HTTP method %s'%request.method
        return redirect('error')



@app.route('/dashboard',methods=('GET',))
def dashboard():
    return render_template('dashboard.html',username=session['username'])

@app.route('/error',methods=('GET',))
def error():
    if 'error' in session.keys():
        msg = session['error']
        del session['error']
        return render_template('error.html',msg=msg)
    return render_template('error.html',msg='An unknown error has occurred')

@app.route('/success',methods('GET',))
def success() :
    if 'success' in session.keys():
        msg = session['success']
        del session['success']
        return render_template('success.html',msg=msg)
