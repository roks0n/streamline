from . import portal as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session

from helpers.decorators import templated


@app.route('/')
def index():
    return render_template('portal/index.html')
