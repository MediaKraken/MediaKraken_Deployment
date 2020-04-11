from sanic_wtf import SanicForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class BSSLoginForm(SanicForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        super(BSSLoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSLoginForm, self).validate()
        if not initial_validation:
            return False
        return True
