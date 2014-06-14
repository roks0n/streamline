#!flask/bin/python
from flask import Flask
from apps.portal import portal
import logging


app = Flask(__name__)

app.register_blueprint(portal)

app.config.from_object('config')

# Logging
file_handler = logging.FileHandler(app.config['BASE_DIR'] + '/var/logs/debug.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)

app.run(debug=True)

