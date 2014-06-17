"""
TODO:
- Activate/Deactivate account
- Edit account
- Add account
"""

from . import admin as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session, flash
from helpers.decorators import templated, guest_required, login_required
from helpers.streamline import get_open_streams, kill_stream, listen_stream
from helpers import rethinkdb as db
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from rethinkdb import now
from passlib.hash import sha256_crypt
from flask import current_app
from forms import UserForm


@app.before_request
def before_request():
    try:
        g.conn = db.connect()
    except RqlDriverError:
        abort(503, "No database connection could be established.")


@app.teardown_request
def teardown_request(exception):
    try:
        g.conn.close()
    except AttributeError:
        pass


@app.route('/')
@login_required
def index():
    # Check for user session
    streams_data = [{
        'client': 'Hud company d.o.o.',
        'hashtags': '#slovenia, #slo'
    },
    {
        'client': 'Facebook',
        'hashtags': '#facebook, #fb'
    }]
    return render_template('adminIndex.html', streams=streams_data, procs=get_open_streams())


@app.route('/users/')
@templated('users.html')
@login_required
def users():
    users_data = db.get_all(current_app.config['DATABASE'], current_app.config['USER_TABLE'])
    return dict(users=users_data)


@app.route('/users/add/', methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserForm(request.form)
    if form.validate_on_submit():
        if not db.username_exist(form.username.data):
            email = form.email.data
            username = form.username.data
            password = sha256_crypt.encrypt(form.password.data)
            role = form.role.data
            user = {
                'username': username,
                'email': email,
                'password': password,
                'date_created': now(),
                'type': role,
                'is_active': True,
            }
            response = db.create_user(user)
            if response['inserted'] == 1:
                return redirect(url_for('admin.users'))
        else:
            flash('This username already exists.', 'error-message')
    return render_template('addUser.html', form=form)


@app.route('/users/edit/<string:username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    user_data = {
        'username': username,
        'email': db.get_user_data(username)['email'],
        'role': db.get_user_data(username)['type']
    }

    form = UserForm(**user_data)

    if request.method == "POST":

        email = form.email.data
        username = form.username.data
        role = form.role.data
        user = {
            'username': username,
            'email': email,
            'type': role,
        }

        if form.password.data:
            password = sha256_crypt.encrypt(form.password.data)
            user['password'] = password
            response = db.update_user(username, email, role, password)
        else:
            response = db.update_user(username, email, role)

        # if response['replaced'] == 1:
        return redirect(url_for('admin.users'))

    return render_template('editUser.html', form=form, username=username)


@app.route('/users/delete/<string:username>')
@login_required
def delete_user(username):
    db.delete_user(username)
    return redirect(url_for('admin.users'))


@app.route('/close_stream/<string:pid>')
@login_required
def close_stream(pid):
    kill_stream(pid)
    return redirect(url_for('admin.index'))


@app.route('/open_stream/<string:hashtags>')
@login_required
def open_stream(hashtags):
    listen_stream(hashtags, 'normal')
    return redirect(url_for('admin.index'))
