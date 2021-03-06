from flask import Blueprint, session, redirect, url_for

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

import views


@admin.before_request
def restrict_bp_to_admins():
    if 'admin' not in session.get('role'):
        return redirect(url_for('site.index'))
