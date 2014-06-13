from flask import Blueprint

portal = Blueprint('portal', __name__)
import views
import admin.views
