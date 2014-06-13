#!flask/bin/python
from flask import Flask
from apps.portal import portal


app = Flask(__name__)
app.config['DEBUG'] = True

app.register_blueprint(portal)

app.run(debug=True)

