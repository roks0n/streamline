from .. import portal as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session

from helpers.decorators import templated
from helpers.utils import redirect_url


@app.route('/admin')
def adminIndex():
    return render_template('admin/index.html')
