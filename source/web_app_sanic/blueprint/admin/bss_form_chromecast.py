from sanic_wtf import SanicForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class BSSChromecastEditForm(SanicForm):
    """
    for editing the chromecast devices
    """
    name = StringField('Name', validators=[DataRequired()])
    ipaddr = StringField('IP Address', validators=[DataRequired()])
    enabled = BooleanField('Enabled')

    def __init__(self, *args, **kwargs):
        super(BSSChromecastEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSChromecastEditForm, self).validate()
        if not initial_validation:
            return False
        return True
