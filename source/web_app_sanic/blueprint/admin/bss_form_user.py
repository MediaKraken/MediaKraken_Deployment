from sanic_wtf import SanicForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class BSSUserEditForm(SanicForm):
    """
    for editing user
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])
    enabled = BooleanField('Enabled')
    is_admin = BooleanField('Admin')

    def __init__(self, *args, **kwargs):
        super(BSSUserEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSUserEditForm, self).validate()
        if not initial_validation:
            return False
        return True
