from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask.ext.github import GitHub
from CONFIG import HOST, PORT, DEBUG, APP_SECRET_KEY, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, DB_LOCATION
from db_helper import UTC_OFFSET
import psycopg2
import datetime
from ast import literal_eval
from operator import attrgetter

from picklesession import PickleSessionInterface
import os

# globals
app  = Flask(__name__)  # instantiate the app here so it can be run as a module
app.config['GITHUB_CLIENT_ID'] = GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = GITHUB_CLIENT_SECRET
app.secret_key = str(APP_SECRET_KEY)

path='/dev/shm/derp_sessions'
if not os.path.exists(path):
    os.mkdir(path)
    os.chmod(path, int('700',8))
app.session_interface=PickleSessionInterface(path)

github = GitHub(app)
conn = psycopg2.connect(DB_LOCATION)
cur  = conn.cursor()

# jinja2 format functions
@app.template_filter('monday')
def format_monday(dt):
    """
    Input: datetime object
    Output: date object representing the monday preceding the input datetime
    """
    return (dt - datetime.timedelta(days = dt.weekday())).date()

@app.template_filter('to_date')
def format_date(dt):
    """
    Input: datetime object
    Output: date object
    """
    return dt.date()


# helper functions
def is_login_ok():
    """
    Check that a login is sensible. Should be checked before rendering any content.
    """
    if 'github_username' not in session:
        # If there isn't a github_username in the session, authentication hasn't been done
        return False
    if 'duck_id' not in session:
        return False

    SQL = "SELECT duck_id,github_username FROM users WHERE github_username=%s and duck_id=%s;"
    data = (session['github_username'],session['duck_id'])
    cur.execute(SQL, data)
    db_row = cur.fetchone()
    if db_row is None:
        return False
    return True

def check_daily():
    """
    Check whether the user has submitted a daily status today, where 'today' is defined
    as the 24-hour period stretching from the prior 0600 to the next 0600.
    """
    # Select only the records for today
    SQL = """SELECT create_dt::TIMESTAMP WITH TIME ZONE AT TIME ZONE 'PST'
FROM dailies
WHERE date_trunc('day',(now()-interval '6 hours')::TIMESTAMP WITH TIME ZONE AT TIME ZONE 'PST') = date_trunc('day',(create_dt-interval '6 hours')::TIMESTAMP WITH TIME ZONE AT TIME ZONE 'PST')
and user_fk=%s"""
    data = (session['user_pk'],)
    cur.execute(SQL, data)
    db_row = cur.fetchone()
    if db_row is None:
        session['daily_completed'] = False
    else:
        session['daily_completed'] = True


def check_weekly():
    """
    Check whether the user has submitted a weekly status this week, where 'this week'
    is defined as the period stretching from the prior 0600 Monday to the next 0600 Monday.
    """
    # Select only the records for this week
    SQL = """SELECT create_dt::TIMESTAMP WITH TIME ZONE AT TIME ZONE 'PST'
FROM weeklies
WHERE date_trunc('week',(now()-interval '6 hours')::TIMESTAMP WITH TIME ZONE AT TIME ZONE 'PST') = date_trunc('week',(create_dt-interval '6 hours')::TIMESTAMP WITH TIME ZONE AT TIME ZONE 'PST')
and user_fk=%s"""
    data = (session['user_pk'],)
    cur.execute(SQL, data)
    db_row = cur.fetchone()
    if db_row is None:
        session['weekly_completed'] = False
    else:
        session['weekly_completed'] = True


def check_pending_reviews():
    """
    Check whether the user has pending code reviews to complete. Puts the pending review
    information into the session.
    """
    SQL = "SELECT review_pk, reviewee_fk FROM code_reviews WHERE (reviewer_fk = %s AND review_dt IS NULL);"
    data = (session['user_pk'],)
    cur.execute(SQL, data)
    res = cur.fetchall()
    app.logger.debug("user pending code reviews query: {}".format(str(res)))
    pending_reviews = []
    for r in res:
        pending_reviews.append( dict(zip(('review_pk', 'reviewee_fk'), r)) )
    for entry in pending_reviews:
        SQL = "SELECT repo FROM users WHERE user_pk = %s;"
        data = (entry['reviewee_fk'],)
        cur.execute(SQL, data)
        res = cur.fetchone()[0]
        entry['url'] = res
    session['pending_reviews'] = pending_reviews
    app.logger.debug("pending reviews session: {}".format(session['pending_reviews']))


# Set "homepage" to index.html
@app.route('/')
@app.route('/index')
def index():
    # Does the session have github credentials? If not go to authentication.
    if not 'github_username' in session:
        return github.authorize()
    # If the user is already signed in, do the credentials match?
    if is_login_ok():
        # User looks alright, let them enter
        return redirect(url_for('dashboard'))
    # Something bad happened... Assume evil.
    return redirect(url_for('logout'))

# get username from homepage input form
@app.route('/signin', methods=['GET', 'POST'])
def signin():

    # this is probably called by a POST from the home page
    if request.method == 'POST':
        duck_id = request.form['duck_id']
        if not duck_id:
            flash("Please try again!")
            return redirect(url_for("index"))

        session['duck_id'] = duck_id

        # handle the login attempt
        if 'logged_in' not in session:

            # check if the user is in the db, and redirect to the correct location
            SQL = "SELECT duck_id FROM users WHERE duck_id = %s;"
            data = (duck_id,)
            cur.execute(SQL, data)
            if not cur.fetchone():
                app.logger.debug("user not in db ... redirecting to signup")
                return redirect(url_for("signup"))
            else:
                app.logger.debug("user found ... redirecting to authorization")
                return github.authorize()

        # else user is already logged in
        else:
            return redirect(url_for("dashboard"))

    # else redirect to the top
    if request.method == 'GET':
        return redirect(url_for("index"))


# github access token getter
@github.access_token_getter
def token_getter():
    return session.get('github_access_token', None)

# handle github authentication
@app.route('/github_callback')
@github.authorized_handler
def authorized(access_token):
    app.logger.debug("entering authoriztion callback")

    if access_token is None:
        flash("Authorization failed!")
        return redirect(url_for("index"))

    # Add github information to the session
    session['github_access_token'] = access_token
    session['github_username'] = github.get('user')['login']

    # Check for the duck_id based on the github username
    SQL = "SELECT duck_id FROM users WHERE github_username=%s;"
    data = (session['github_username'],)
    cur.execute(SQL, data)
    db_row = cur.fetchone()

    if db_row is None:
        # No user registered in the DB... Go to the signup page.
        return redirect(url_for('signup'))

    db_duck_id = db_row[0]
    app.logger.debug("db duck_id: {}".format(db_duck_id))
    session['logged_in'] = db_duck_id
    session['duck_id']   = db_duck_id

    return redirect(url_for("dashboard"))


# display dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not is_login_ok():
        msg = "login failure: something is wrong with the session ... try logging in again"
        return redirect(url_for("logout", logout_message = msg))


    # put the user's id from the db into the session
    #   NOTE: all other methods assume that the user_pk has been put into the session
    if 'user_pk' not in session:
        SQL = "SELECT user_pk FROM users WHERE duck_id = %s;"
        data = (session['duck_id'],)
        cur.execute(SQL, data)
        user_pk = cur.fetchone()[0]
        app.logger.debug("setting user_pk: " + str(user_pk))
        session['user_pk'] = user_pk

    # check if the user has submitted a daily status update
    check_daily()

    # check if the user has submitted a weekly status update
    check_weekly()

    # check for pending code reviews
    check_pending_reviews()

    # display the dashboard page
    return render_template('dashboard.html')


# display profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not is_login_ok():
        msg = "login failure: something is wrong with the session ... try logging in again"
        return redirect(url_for("logout", logout_message = msg))

    # if we are getting a POST, handle it
    if request.method == 'POST':

        # handle profile info submission
        if 'repo' in request.form and 'email' in request.form:
            repo_msg = request.form['repo']
            email_msg = request.form['email']

            SQL = "UPDATE users SET repo=%s, email=%s WHERE (user_pk=%s);"
            data = (repo_msg, email_msg, session['user_pk'])
            cur.execute(SQL, data)
            conn.commit()

