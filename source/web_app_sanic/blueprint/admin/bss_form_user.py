from sanic_wtf import SanicForm as Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class UserEditForm(Form):
    """
    for editing user
    """
    username = TextField('Username',
                         validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email',
                      validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])
    enabled = BooleanField('Enabled')
    is_admin = BooleanField('Admin')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(UserEditForm, self).validate()
        if not initial_validation:
            return False
        return True
