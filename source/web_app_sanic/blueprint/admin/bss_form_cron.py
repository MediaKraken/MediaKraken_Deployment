from decimal import ROUND_UP

from sanic_wtf import SanicForm
from wtforms import TextField, TextAreaField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired


class CronEditForm(SanicForm):
    """
    for editing the cron jobs
    """
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    enabled = BooleanField('Enabled')
    interval = SelectField('Interval', choices=[('Minutes', 'Minutes'), ('Hours', 'Hours'),
                                                ('Days', 'Days'), ('Weekly', 'Weekly')])
    time = DecimalField('Time', places=2, rounding=ROUND_UP)

    def __init__(self, *args, **kwargs):
        super(CronEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(CronEditForm, self).validate()
        if not initial_validation:
            return False
        return True
