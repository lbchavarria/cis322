from flask import Flask, render_template, request, session, redirect
from config import dbname, dbhost, dbport
import json
import psycopg2
import datetime

app = Flask(__name__)

app.secret_key = 'SECRETKEY'



#@app.route('/create_user',methods=('GET','POST'))
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
                sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s AND active=TRUE"
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
        cur.execute(sql,(usern,))
        res = cur.fetchone()[0]
        if res != 0:
            is_log_off = True
        else:
            is_log_off = False
        connect.commit()
    to_approve = None
    to_load = None
    if not is_log_off:
        with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
            cur = connect.cursor()
            sql = "SELECT transit_id,request_time,asset_tag,f1.name,f2.name FROM trans_request JOIN assets ON assets.asset_id=trans_request.asset_fk JOIN facilities f1 ON f1.facility_id=trans_request.source JOIN facilities f2 ON f2.facility_id=trans_request.destination WHERE is_approved IS NULL ORDER BY trans_request.request_time ASC"
            cur.execute(sql)
            connect.commit()
            res = cur.fetchall()
            l = list()
            for i in res:
                d = dict()
                d['id'] = i[0]
                d['date'] = i[1]
                d['asset_tag'] = i[2]
                d['source'] = i[3]
                d['dest'] = i[4]
                l.append(d)
        to_approve = l
    if is_log_off:
        with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
            cur = connect.cursor()
            sql = "SELECT transit_id,request_time,asset_tag,f1.name,f2.name FROM trans_request JOIN assets ON assets.asset_id=trans_request.asset_fk JOIN facilities f1 ON f1.facility_id=trans_request.source JOIN facilities f2 ON f2.facility_id=trans_request.destination WHERE is_approved IS True AND unload IS NULL ORDER BY trans_request.request_time ASC"
            cur.execute(sql)
            connect.commit()
            res = cur.fetchall()
            l = list()
            for i in res:
                d = dict()
                d['id'] = i[0]
                d['date'] = i[1]
                d['asset_tag'] = i[2]
                d['source'] = i[3]
                d['dest'] = i[4]
                l.append(d)
        to_load = l
    return render_template('dashboard.html',username=session['username'],is_log_off=is_log_off, to_approve=to_approve, to_load=to_load)

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
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
        cur = connect.cursor()
        sql = "SELECT COUNT(*) FROM users WHERE username=%s"
        cur.execute(sql,(username,))
        res = cur.fetchone()[0]
        if res != 1:
            return "User can't add facility"
        sql = "SELECT COUNT(*) FROM facilities WHERE code=%s OR name=%s"
        cur.execute(sql,(code,name))
        res = cur.fetchone()[0]
        if res != 0:
            return "Already exists and won't be added again"
        sql = "INSERT INTO facilities (name,code,user_fk) SELECT %s,%s,user_id FROM users WHERE username=%s"
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
                facility_list.append(d)
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
        cur.execute(sql,(username,))
        res = cur.fetchone()[0]
        if res != 1:
            return "User can't add asset"
        sql = "SELECT COUNT(*) FROM assets WHERE asset_tag=%s"
        cur.execute(sql,(tag,))
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
        cur.execute(sql,(session['username'],))
        connect.commit()
        if role == cur.fetchone()[0]:
            return True
    return False

def delete_asset(tag,date):
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
        cur = connect.cursor()
        sql = "SELECT COUNT(*) FROM assets WHERE asset_tag=%s"
        cur.execute(sql,(tag,))
        res = cur.fetchone()[0]
        if res != 1:
            return 'The asset tag %s does not exist in the database'%tag
        sql = 'SELECT COUNT(*) FROM asset_at JOIN assets ON assets.asset_id=asset_at.asset_fk WHERE assets.asset_tag=%s AND disposed IS NOT NULL'
        cur.execute(sql,(tag,))
        res = cur.fetchone()[0]
        if res > 0:
            return 'The asset tag %s has already been disposed'%tag
        sql = "UPDATE asset_at SET disposed=%s FROM assets WHERE asset_fk=asset_id AND asset_tag=%s AND depart IS NULL AND disposed IS NULL"
        cur.execute(sql,(date,tag))
        connect.commit()
        return None

@app.route('/dispose_asset',methods=('GET','POST'))
def dispose_asset():
    if not is_user(1):
        session['error']='Logistic Officers are the only ones that can dispose assets'
        return redirect('error')
    if request.method=='GET':
        return render_template('dispose_asset.html',rdate=datetime.datetime.utcnow().isoformat())
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
                sql += " ORDER BY asset_tag ASC"
                cur.execute(sql,(fields['rdate'],fields['rdate'],fields['rdate']))
            else:
                sql += " AND facilities.code=%s ORDER BY asset_tag ASC"
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

@app.route('/transfer_req',methods=('GET','POST'))
def transfer_req():
    if not is_user(1):
        session['error']='Logistic Officers are the only ones that can request a transfer'
        return redirect('error')
    if request.method=='GET':
        return render_template('transfer_req.html')
    if request.method=='POST':
        with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
            cur = connect.cursor()
            sql = "SELECT COUNT(*) FROM assets WHERE asset_tag=%s"
            asset_tag = request.form['asset_tag']
            cur.execute(sql,(asset_tag,))
            connect.commit()
            res = cur.fetchone()[0]
            if res != 1:
                session['error'] = 'The asset tag does not exist'
                return redirect('error')
            sql = "SELECT COUNT(*) FROM facilities WHERE name=%s"
            source = request.form['source']
            cur.execute(sql,(source,))
            connect.commit()
            res = cur.fetchone()[0]
            if res != 1:
                session['error'] = "The source facility does not exist"
                return redirect('error')
            sql = "SELECT COUNT(*) FROM assets JOIN asset_at ON assets.asset_id=asset_at.asset_fk JOIN facilities ON facilities.facility_id=asset_at.facility_fk WHERE asset_tag=%s AND name=%s"
            cur.execute(sql,(asset_tag,source))
            connect.commit()
            res = cur.fetchone()[0]
            if res != 1:
                session['error']='The asset does not exist in the source facility'
                return redirect('error')
            sql = "SELECT COUNT(*) FROM facilities WHERE name=%s"
            dest = request.form['dest']
            cur.execute(sql,(dest,))
            connect.commit()
            res = cur.fetchone()[0]
            if res != 1:
                session['error'] = "The destination facility does not exist"
                return redirect('error')
            sql = "INSERT INTO trans_request (requester_id,request_time,source,destination,asset_fk) SELECT user_id,now(),f1.facility_id,f2.facility_id,asset_id FROM users, facilities AS f1, facilities AS f2, assets WHERE username=%s AND f1.name=%s AND f2.name=%s AND asset_tag=%s"
            username=session['username']
            cur.execute(sql,(username,source,dest,asset_tag))
            connect.commit()
            session['success'] = "Request has been successully added"
            return redirect('success')

@app.route('/approve_req', methods=('GET','POST'))
def approve_req():
    if not is_user(2):
        session['error']='Facility Officers are the only ones to approve or reject transfer requests'
        return redirect('error')
    if request.method=='GET':
        print(request.args)
        if not 'id' in request.args:
            print("no id")
            session['error']='Invalid Request'
            return redirect('error')
        else:
            transit_id=int(request.args['id'])
            try:
                with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
                    cur = connect.cursor()
                    sql = "SELECT transit_id,asset_tag,f1.name,f2.name,load,load_by,unload,unload_by,is_approved FROM trans_request JOIN assets ON assets.asset_id=trans_request.asset_fk JOIN facilities f1 ON f1.facility_id=trans_request.source JOIN facilities f2 ON f2.facility_id=trans_request.destination WHERE transit_id=%s"
                    cur.execute(sql,(transit_id,))
                    connect.commit()
                    res=cur.fetchone()
                    d=dict()
                    d['id']=res[0]
                    d['asset_tag']=res[1]
                    d['source']=res[2]
                    d['dest']=res[3]
                    d['load']=res[4]
                    d['load_by']=res[5]
                    d['unload']=res[6]
                    d['unload_by']=res[7]
                    d['is_approved']=res[8]
                data=d
            except:
                print("database error")
                session['error']="Invalid Request"
                return redirect ('error')
            if not data['is_approved']==None:
                session['error']='Approval has already been completed'
                return redirect('error')
            return render_template('approve_req.html',data=data)
    if request.method=='POST':
        if not 'id' in request.form or not 'submit' in request.form:
            session['error']='Invalid Request'
            return redirect('error')
        if request.form['submit']=='cancel':
            pass
        if request.form['submit']=='approve':
            with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
                cur = connect.cursor()
                sql = "UPDATE trans_request SET (approver_id,approval_time,is_approved)=(user_id,now(),True) FROM users WHERE username=%s AND transit_id=%s"
                cur.execute(sql,(session['username'],int(request.form['id'])))
                connect.commit()
        if request.form['submit']=='reject':
            with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
                cur = connect.cursor()
                sql = "UPDATE trans_request SET (approver_id,approval_time,is_approved)=(user_id,now(),False) FROM users WHERE username=%s AND transit_id=%s"
                cur.execute(sql,(session['username'],int(request.form['id'])))
                connect.commit()
        return redirect('dashboard')

@app.route('/update_transit', methods=('GET','POST'))
def update_transit():
    if not is_user(1):
        session['error']='Logistics Officers are the only ones update the transit'
        return redirect('error')
    if request.method=='GET':
        print(request.args)
        if not 'id' in request.args:
            print("no id")
            session['error']='Invalid Request'
            return redirect('error')
        else:
            transit_id=int(request.args['id'])
            try:
                with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
                    cur = connect.cursor()
                    sql = "SELECT transit_id,asset_tag,f1.name,f2.name,load,unload FROM trans_request JOIN assets ON assets.asset_id=trans_request.asset_fk JOIN facilities f1 ON f1.facility_id=trans_request.source JOIN facilities f2 ON f2.facility_id=trans_request.destination WHERE transit_id=%s"
                    cur.execute(sql,(transit_id,))
                    connect.commit()
                    res=cur.fetchone()
                    d=dict()
                    d['id']=res[0]
                    d['asset_tag']=res[1]
                    d['source']=res[2]
                    d['dest']=res[3]
                    d['load']=res[4]
                    d['unload']=res[5]
                data=d
            except:
                print("database error")
                session['error']="Invalid Error"
                return redirect('error')
            if not data['unload']==None:
                session['error']='Asset has already been unloaded'
                return redirect('error')
        return render_template("update_transit.html",data=data)
    if request.method=='POST':
        load = request.form['load']
        unload = request.form['unload']
        if request.form['submit']=='cancel':
            pass
        if request.form['submit']=='save':
            with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
                cur = connect.cursor()
                sql = "UPDATE trans_request SET load=%s,unload=%s,load_by=user_id,unload_by=user_id FROM users WHERE username=%s"
                cur.execute(sql,(load,unload,session['username']))
                connect.commit()
        return redirect('dashboard')

@app.route('/activate_user', methods=('POST',))
def activate_user():
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
        cur=connect.cursor()
        username = request.form['username']
        password = request.form['password']
        print("1")
        if request.form['role'] == 'facofc':
            role_id = 2
        elif request.form['role'] == 'logofc':
            role_id = 1
        print("2")
        sql = "SELECT COUNT(*) FROM users WHERE username=%s"
        cur.execute(sql,(username,))
        connect.commit()
        res = cur.fetchone()[0]
        print("3")
        if res != 0:
            sql = "UPDATE users SET password=%s, active=TRUE WHERE username=%s"
            cur.execute(sql,(password,username))
            connect.commit()
            print("4")
            return "The user has been activated"
        elif res == 0:
            sql = "INSERT INTO users (username, password, role_fk, active) VALUES (%s,%s,%s,TRUE)"
            cur.execute(sql,(username,password,role_id))
            connect.commit()
            print("4")
            return "The user has been added"

@app.route('/revoke_user', methods=('POST',))
def revoke_user():
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as connect:
        cur=connect.cursor()
        username=request.form['username']
        sql = "UPDATE users SET active=FALSE WHERE username=%s"
        cur.execute(sql,(username,))
        connect.commit()
        return "The user has been revoked"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
