#!flask/bin/python
from flask import Flask
from apps.portal import portal


app = Flask(__name__)

app.register_blueprint(portal)

app.config.from_object('config')

app.run(debug=True)

