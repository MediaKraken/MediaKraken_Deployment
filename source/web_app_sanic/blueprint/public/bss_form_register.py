from sanic_wtf import SanicForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class BSSRegisterForm(SanicForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address',
                        validators=[DataRequired(), Email(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(),
                                          EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(BSSRegisterForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSRegisterForm, self).validate()
        if not initial_validation:
            return False
        return True
