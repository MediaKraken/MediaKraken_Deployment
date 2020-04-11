from sanic_wtf import SanicForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class BSSRegisterForm(SanicForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(BSSRegisterForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSRegisterForm, self).validate()
        if not initial_validation:
            return False
        return True
