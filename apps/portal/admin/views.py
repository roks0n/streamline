from .. import portal as app
from flask import Flask, redirect, url_for, g, jsonify, request, abort, session

from helpers.decorators import templated
from helpers.streamline import get_open_streams


@app.route('/admin')
@templated('admin/index.html')
def adminIndex():
    return dict(procs=get_open_streams())
