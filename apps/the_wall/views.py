from . import the_wall as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session
from helpers.decorators import templated, guest_required, login_required
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


@app.route('/', defaults={'stream_id': '12345667890'})
@app.route('/<string:stream_id>')
def wallIndex(stream_id):
    query = {'stream_id': '1234567890'}
    tweets_data = db.get_filter(current_app.config['DATABASE'], current_app.config['TWEETS_TABLE'], query, 10, 'created_at')
    # print tweets_data
    return render_template('wallIndex.html', tweets=tweets_data)
