from sanic_wtf import SanicForm
from wtforms import BooleanField


class BackupEditForm(SanicForm):
    """
    for editing backups
    """
    enabled = BooleanField('Enabled')

    # interval = SelectField('Interval', choices=[('Hours', 'Hours'),\
    # ('Days', 'Days'), ('Weekly', 'Weekly')])
    # time = DecimalField('Time', places = 2, rounding=ROUND_UP)

    def __init__(self, *args, **kwargs):
        super(BackupEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BackupEditForm, self).validate()
        if not initial_validation:
            return False
        return True