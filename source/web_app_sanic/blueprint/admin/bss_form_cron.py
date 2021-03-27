from decimal import ROUND_UP

from sanic_wtf import SanicForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired


class BSSCronEditForm(SanicForm):
    """
    for editing the cron jobs
    """
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    enabled = BooleanField('Enabled')
    interval = SelectField('Interval', choices=[('Minutes', 'Minutes'), ('Hours', 'Hours'),
                                                ('Days', 'Days'), ('Weekly', 'Weekly')])
    time = DecimalField('Time', places=2, rounding=ROUND_UP)

    def __init__(self, *args, **kwargs):
        super(BSSCronEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSCronEditForm, self).validate()
        if not initial_validation:
            return False
        return True
