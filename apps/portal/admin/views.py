from .. import portal as app
from flask import Flask, redirect, url_for, g, jsonify, request, abort, session
from helpers.decorators import templated, guest_required, login_required
from helpers.streamline import get_open_streams, kill_stream, listen_stream
from helpers import rethinkdb as db
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from rethinkdb import now
from passlib.hash import sha256_crypt
from flask import current_app


@app.before_request
def before_request():
    try:
        g.conn = db.connect()
    except RqlDriverError:
        abort(503, "No database connection could be established.")

    # Just for the first time TODO: make something more convenient (maybe put it in run.py)
    # db.table_create(current_app.config['DATABASE'], current_app.config['USER_TABLE'], primary_key='username')


@app.teardown_request
def teardown_request(exception):
    try:
        g.conn.close()
    except AttributeError:
        pass


@app.route('/admin/')
@templated('admin/index.html')
@login_required
def adminIndex():
    user = session.get('username')
    streams_data = [{
        'client': 'Hud company d.o.o.',
        'hashtags': '#slovenia, #slo'
    },
    {
        'client': 'Facebook',
        'hashtags': '#facebook, #fb'
    }]
    return dict(procs=get_open_streams(), streams=streams_data)


@app.route('/admin/close_stream/<string:pid>')
def close_stream(pid):
    kill_stream(pid)
    return redirect(url_for('.adminIndex'))


@app.route('/admin/open_stream/<string:hashtags>')
def open_stream(hashtags):
    listen_stream(hashtags, 'background')
    return redirect(url_for('.adminIndex'))


@app.route('/admin/signup/', methods=['GET', 'POST'])
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
            return redirect(url_for('portal.adminIndex'))
        if response['error'] == 1:
            return dict(error=True)


@app.route('/admin/login/', methods=['GET', 'POST'])
@templated('login.html')
@guest_required
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        hash = db.get_password(username)
        if sha256_crypt.verify(password, hash):
            session['username'] = username
            return redirect(url_for('portal.adminIndex'))


@app.route('/admin/logout/')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('portal.adminIndex'))
