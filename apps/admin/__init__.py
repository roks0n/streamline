from flask import Blueprint, session, redirect, url_for
import views

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')


@admin.before_request
def restrict_bp_to_admins():
    if 'admin' not in session.get('role'):
        return redirect(url_for('site.index'))
