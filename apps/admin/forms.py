from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import Required, Email, EqualTo


class UserForm(Form):
    email = TextField('Email', [Email(), Required(message='Forgot your email address?')])

    username = TextField('Username', [Required(message='Enter a username.')])

    password = PasswordField('Password', [Required(message='You must provide a password.')])

    role = SelectField('Role', default='user', choices=[('user', 'User'), ('admin', 'Admin')])
