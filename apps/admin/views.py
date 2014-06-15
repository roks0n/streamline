"""
TODO:
- Activate/Deactivate account
- Edit account
- Add account
"""

from . import admin as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session
from helpers.decorators import templated, guest_required, login_required
from helpers.streamline import get_open_streams, kill_stream, listen_stream
from helpers import rethinkdb as db
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import current_app


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
