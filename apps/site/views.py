from . import site as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session, current_app
from helpers import rethinkdb as db
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from rethinkdb import now
from passlib.hash import sha256_crypt
from helpers.decorators import templated, guest_required, login_required


@app.before_request
def before_request():
    try:
        g.conn = db.connect()
    except RqlDriverError:
        abort(503, "No database connection could be established.")

    # just for setup (this needs to be moved and checked elsewhere more conveniente)
    # db.db_create(constants.DB)
    # db.table_create(constants.DB, constants.USERS_TABLE, primary_key='username')
    # db.table_create(current_app.config['DATABASE'], current_app.config['TWEETS_TABLE'], primary_key='id')

@app.teardown_request
def teardown_request(exception):
    try:
        g.conn.close()
    except AttributeError:
        pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup/', methods=['GET', 'POST'])
@templated('signup.html')
@guest_required
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('passwd')

        print request.form

        if db.username_exist(username):
            return dict(error=True)
        if db.email_exist(email):
            return dict(error=True)


        hash = sha256_crypt.encrypt(password)

        user = {
            'username': username,
            'email': email,
            'password': hash,
            'date_created': now(),
            'type': 'user',
            'is_active': True,
        }
        response = db.create_user(user)
        if response['inserted'] == 1:
            session['username'] = username
            return redirect(url_for('site.signup'))
        if response['error'] == 1:
            return dict(error=True)


@app.route('/login/', methods=['GET', 'POST'])
@templated('login.html')
@guest_required
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            hash = db.get_password(username)
            if sha256_crypt.verify(password, hash):
                session['username'] = username
                # TODO: fetch user role aka. type and put it in session
                session['role'] = 'admin'
        return redirect(url_for('site.login'))


@app.route('/logout/')
@login_required
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('site.index'))
