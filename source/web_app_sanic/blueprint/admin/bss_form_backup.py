import decimal

from sanic_wtf import SanicForm
from wtforms import BooleanField
from wtforms import DecimalField
from wtforms import SelectField
from wtforms import SubmitField


class BSSBackupEditForm(SanicForm):
    """
    for editing backups
    """
    enabled = BooleanField('Enable automatic backup')
    interval = SelectField('Interval', choices=[('Hours', 'Hours'),
                                                ('Days', 'Days'),
                                                ('Weekly', 'Weekly')])
    time = DecimalField('Time', places=2, rounding=decimal.ROUND_UP)
    # TODO backup class, ie cloud, etc
    submit = SubmitField('Submit Backup')

    def __init__(self, *args, **kwargs):
        super(BSSBackupEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSBackupEditForm, self).validate()
        if not initial_validation:
            return False
        return True
