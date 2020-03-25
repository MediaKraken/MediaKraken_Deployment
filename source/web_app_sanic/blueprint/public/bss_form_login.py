from wtforms import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class BSSLoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
