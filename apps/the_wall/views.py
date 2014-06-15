from . import the_wall as app
from flask import Flask, redirect, url_for, g, jsonify, render_template, request, abort, session
from helpers.decorators import templated, guest_required, login_required


@app.route('/')
def wallIndex():
    return render_template('wallIndex.html')
