from sanic_wtf import SanicForm as Form
from wtforms import BooleanField


class DLNAEditForm(Form):
    """
    for editing dlna
    """
    enabled = BooleanField('Enabled')

    def __init__(self, *args, **kwargs):
        super(DLNAEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(DLNAEditForm, self).validate()
        if not initial_validation:
            return False
        return True
