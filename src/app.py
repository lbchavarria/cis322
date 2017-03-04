from flask import Flask, render_template, request, session, redirect
from config import dbname, dbhost, dbport
import json
import psycopg2
import datetime

app = Flask(__name__)

app.secret_key = 'SECRETKEY'



@app.route('/create_user',methods=('GET','POST'))
def create_user():
    if request.method=='GET':
        return render_template('create_user.html')
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
                cur = connect.cursor()
                sql = "SELECT COUNT(*) FROM users WHERE username=%s"
                cur.execute(sql,(username,))
                connect.commit()
                res = cur.fetchone()[0]
                if res != 0:
                    session['error'] = 'The username %s is already taken'%username
                    return redirect('error')
                sql = "INSERT INTO users (username,password,role_fk) VALUES (%s,%s,%s)"
                cur.execute(sql,(username,password,role))
                connect.commit()
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
            with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
                cur = connect.cursor()
                sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
                cur.execute(sql,(username,password))
                connect.commit()
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

@app.route('/dashboard',methods=('GET','POST'))
def dashboard():
    usern = session['username']
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
        cur = connect.cursor()
        sql = "SELECT COUNT(*) FROM users WHERE username=%s AND role_fk=1"
        cur.execute(sql,(usern))
        res = cur.fetchone()[0]
        if res != 0:
            is_log_off = True
        else:
            is_log_off = False
        connect.commit()
    return render_template('dashboard.html',username=session['username'],is_log_off=is_log_off)

@app.route('/error',methods=('GET','POST'))
def error():
    if 'error' in session.keys():
        msg = session['error']
        del session['error']
        return render_template('error.html',msg=msg)
    return render_template('error.html',msg='An unknown error has occurred')

@app.route('/success',methods=('GET','POST'))
def success() :
    if 'success' in session.keys():
        msg = session['success']
        del session['success']
        return render_template('success.html',msg=msg)

def into_facility(code,name,username):
    with psycopg2.connect(dbname=dbname,host=dbhost,post=dbpost) as connect:
        cur = connect.cursor()
        sql = "SELECT COUNT(*) FROM users WHERE username=%s"
        cur.execute(sql,(username))
        res = cur.fetchone()[0]
        if res != 1:
            return "User can't add facility"
        sql = "SELECT COUNT(*) FROM facilities WHERE code=%s OR name=%s"
        cur.execute(sql,(code,name))
        res = cur.fetchone()[0]
        if res != 0:
            return "Already exists and won't be added again"
        sql = "INSERT INTO facilities (name,fcode,user_fk) SELECT %s,%s,user_id FROM users WHERE username=%s"
        cur.execute(sql,(name,code,username))
        connect.commit()
    return None

@app.route('/add_facility',methods=('GET','POST'))
def add_facility():
    if request.method=='GET':
        with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
            cur = connect.cursor()
            sql = "SELECT code,name,username FROM facilities JOIN users ON users.user_id=facilities.user_fk ORDER BY code"
            cur.execute(sql)
            connect.commit()
            res = cur.fetchall()
            facility_list = list()
            for i in res:
                d = dict()
                d['code'] = i[0]
                d['name'] = i[1]
                d['username'] = i[2]
                facilities.append(d)
        return render_template('add_facility.html',facility_list=facility_list)
    if request.method=='POST':
        if not 'username' in session:
            username = 'system'
        else:
            username = session['username']
        code = request.form['code']
        name = request.form['name']
        res = into_facility(code,name,username)
        if res is not None:
            if res == "User can't add facility":
                del session['username']
            session['error']=res
            return redirect('error')
        return redirect('add_facility')

def into_asset(tag,desc,code,username):
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
        cur = connect.cursor()
        sql = "SELECT COUNT(*) FROM users WHERE username=%s"
        cur.execute(sql,(username))
        res = cur.fetchone()[0]
        if res != 1:
            return "User can't add asset"
        sql = "SELECT COUNT(*) FROM assets WHERE asset_tag=%s"
        cur.execute(sql,(tag))
        res= cur.fetchone()[0]
        if res != 0:
            return "Already exists and won't be added again"
        sql = "INSERT INTO assets (asset_tag,description,user_fk) SELECT %s,%s,user_id FROM users WHERE username=%s RETURNING asset_id"
        cur.execute(sql,(tag,desc,username))
        asset_id = cur.fetchone()[0]
        sql = "INSERT INTO asset_at (asset_fk,facility_fk,arrive) SELECT %s,facility_id,now() FROM facilities WHERE code=%s"
        cur.execute(sql,(asset_id,code))
        connect.commit()
    return None

def select_codes(selected=''):
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
        cur = connect.cursor()
        sql = "SELECT code,name FROM facilities ORDER BY name"
        cur.execute(sql)
        connect.commit()
        res = cur.fetchall()
        code_options = list()
        for i in res:
            if i[0]==selected:
                code_options.append('<option value=%s" selected>%s</option>'%(i[0],i[1]))
            else:
                code_options.append('<option value=%s>%s</option>'%(i[0],i[1]))
        return ''.join(code_options)


@app.route('/add_asset',methods=('GET','POST'))
def add_asset():
    if request.method=='GET':
        with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
            cur = connect.cursor()
            sql = "SELECT asset_tag,description,username FROM assets JOIN users ON users.user_id=assets.user_fk ORDER BY asset_tag"
            cur.execute(sql)
            connect.commit()
            res = cur.fetchall()
            asset_list = list()
            for i in res:
                d = dict()
                d['tag'] = i[0]
                d['desc'] = i[1]
                d['username'] = i[2]
                asset_list.append(d)
        code_options = select_codes()
        return render_template('add_asset.html',asset_list=asset_list,code_options=code_options)
    if request.method=='POST':
        if not 'username' in session:
            username = 'system'
        else:
            username = session['username']
        tag = request.form['tag']
        desc = request.form['desc']
        code = request.form['code']
        res = into_asset(tag,desc,code,username)
        if res is not None:
            if res == "User can't add asset":
                del session['username']
            session['error']=res
            return redirect('error')
        return redirect('add_asset')

def is_user(role):
    if not 'username' in session:
        return False
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
        cur = connect.cursor()
        sql = "SELECT role_fk FROM users WHERE username=%s"
        cur.execute(sql,(session['username']))
        connect.commit()
        if role == cur.fetchone()[0]:
            return True
    return False

def delete_asset(tag,date):
    with psycopg2.connect(dbname=dbname,host=dbhost,post=dbpost) as connect:
        cur = connect.cursor()
        sql = "SELECT COUNT(*) FROM assets WHERE asset_tag=%s"
        cur.execute(sql,(tag))
        res = cur.fetchone()[0]
        if res != 1:
            return 'The asset tag %s does not exist in the database'%tag
        sql = 'SELECT COUNT(*) FROM asset_at JOIN assets ON assets.asset_id=asset_at.asset_fk WHERE assets.asset_tag=%s AND disposed IS NOT NULL'
        cur.execute(sql,(tag))
        res = cur.fetchone()[0]
        if res > 0:
            return 'The asset tag %s has already been disposed'%tag
        sql = "UPDATE asset_at SET disposed=%s FROM assets WHERE asset_fk=asset_id AND asset_tag=%s AND depart IS NULL AND disposed IS NULL"
        cur.execute(sql,(date,tag))
        connect.commit()
        return None

@app.route('/dispose_asset',methods=('GET','POST'))
def dispose_asset():
    if not is_user('1'):
        session['error']='Logistic Officers are the only ones that can dispose assets'
        return redirect('error')
    if request.method=='GET':
        return render_template('dispose_asset.html')
    if request.method=='POST':
        tag = request.form['tag']
        date = request.form['date']
        res = delete_asset(tag,date)
        if res is not None:
            session['error']=res
            return redirect('error')
        return redirect('dashboard')

@app.route('/asset_report',methods=('GET','POST'))
def asset_report():
    fields=dict()
    data=list()
    if request.method=='GET':
        fields['code']=''
        fields['rdate']=datetime.datetime.utcnow().isoformat()
    if request.method=='POST':
        if 'code' in request.form and 'date' in request.form:
            fields['code']=request.form['code']
            fields['rdate']=request.form['date']
        else:
            fields['code']=None
            fields['rdate']=datetime.datetime.utcnow().isoformat()
        with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
            cur = connect.cursor()
            sql = 'SELECT asset_tag,description,name,arrive,depart,disposed,code FROM asset_at JOIN facilities ON asset_at.facility_fk=facilities.facility_id JOIN assets ON asset_at.asset_fk=assets.asset_id WHERE (arrive IS NULL OR arrive<=%s) AND (depart IS NULL OR depart>=%s) AND (disposed IS NULL OR disposed>=%s)'
            if fields['code']=='':
                sql += " OREDR BY asset_tag ASC"
                cur.execute(sql,(fields['rdate'],fields['rdate'],fields['rdate']))
            else:
                sql += " AND facilities.code=%s OREDR BY asset_tag ASC"
                cur.execute(sql,(fields['rdate'],fields['rdate'],fields['rdate'],fields['code']))
            res = cur.fetchall()
            connect.commit()
            for i in res:
                d=dict()
                d['asset_tag']=i[0]
                d['desc']=i[1]
                d['name']=i[2]
                if i[3] is None:
                    d['adate']=''
                else:
                    d['adate']=i[3]
                if i[4] is None and i[5] is None:
                    d['ddate']=''
                elif i[4]:
                    d['ddate']=i[4]
                else:
                    d['ddate']=i[5]
                d['code']=i[6]
                data.append(d)
    v=select_codes(selected=fields['code'])
    return render_template('asset_report.html',vals=fields,code_options=v,data=data)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
