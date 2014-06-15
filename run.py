#!flask/bin/python
from flask import Flask
from apps.admin import admin
from apps.site import site
from apps.the_wall import the_wall
import logging


app = Flask(__name__)
app.config.from_object('config')


# Blueprints
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(the_wall, url_prefix='/wall')
app.register_blueprint(site, url_prefix='')

# Logging
file_handler = logging.FileHandler(app.config['BASE_DIR'] + '/var/logs/debug.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)

app.run(debug=True)

