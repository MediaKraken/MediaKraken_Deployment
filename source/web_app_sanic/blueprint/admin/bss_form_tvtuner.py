from sanic_wtf import SanicForm
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired


class TVTunerEditForm(SanicForm):
    """
    for editing the tvtuner devices
    """
    name = TextField('Name', validators=[DataRequired()])
    ipaddr = TextField('IP Address', validators=[DataRequired()])
    enabled = BooleanField('Enabled')

    def __init__(self, *args, **kwargs):
        super(TVTunerEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(TVTunerEditForm, self).validate()
        if not initial_validation:
            return False
        return True
