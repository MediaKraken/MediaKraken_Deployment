from sanic_wtf import SanicForm
from wtforms import StringField


class BSSSearchForm(SanicForm):
    """
    for searching media
    """
    search_text = StringField('Search For')

    def __init__(self, *args, **kwargs):
        super(BSSSearchForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSSearchForm, self).validate()
        if not initial_validation:
            return False
        return True
