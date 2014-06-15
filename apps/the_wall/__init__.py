from flask import Blueprint

the_wall = Blueprint('the_wall', __name__, static_folder='static', template_folder='templates')
import views
