from sanic_wtf import SanicForm
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired


class ChromecastEditForm(SanicForm):
    """
    for editing the chromecast devices
    """
    name = TextField('Name', validators=[DataRequired()])
    ipaddr = TextField('IP Address', validators=[DataRequired()])
    enabled = BooleanField('Enabled')

    def __init__(self, *args, **kwargs):
        super(ChromecastEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(ChromecastEditForm, self).validate()
        if not initial_validation:
            return False
        return True
