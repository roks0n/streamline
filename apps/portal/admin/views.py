from .. import portal as app
from flask import Flask, redirect, url_for, g, jsonify, request, abort, session

from helpers.decorators import templated
from helpers.streamline import get_open_streams, kill_stream, listen_stream
from helpers import rethinkdb as db
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from passlib.hash import sha256_crypt


@app.route('/admin')
@templated('admin/index.html')
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
