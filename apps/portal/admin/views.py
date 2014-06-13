from .. import portal as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session

from helpers.decorators import templated
from helpers.utils import redirect_url


@app.route('/admin')
@templated('admin/index.html')
def adminIndex():
    # procs_data = [{
    #     'pid': '1',
    #     'start_time': '2014-21-2 14:00:00',
    #     'hashtags': '#test'
    # },
    # {
    #     'pid': '2',
    #     'start_time': '2014-21-2 11:52:00',
    #     'hashtags': '#moar'
    # },
    # {
    #     'pid': '3',
    #     'start_time': '2014-20-2 14:52:00',
    #     'hashtags': '#testingmore'
    # }]
    data = 'test'
    return dict(collection=data)
