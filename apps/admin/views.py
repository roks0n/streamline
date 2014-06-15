from . import admin as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session
from helpers.decorators import templated, guest_required, login_required
from helpers.streamline import get_open_streams, kill_stream, listen_stream
from helpers import rethinkdb as db
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import current_app


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


@app.route('/close_stream/<string:pid>')
@login_required
def close_stream(pid):
    kill_stream(pid)
    return redirect(url_for('admin.index'))


@app.route('/open_stream/<string:hashtags>')
@login_required
def open_stream(hashtags):
    listen_stream(hashtags, 'background')
    return redirect(url_for('admin.index'))
