from flask import Blueprint

site = Blueprint('site', __name__, static_folder='../../compressed/site', template_folder='templates')
import views
