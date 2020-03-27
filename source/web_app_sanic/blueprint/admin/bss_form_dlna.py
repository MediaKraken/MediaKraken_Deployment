from sanic_wtf import SanicForm
from wtforms import BooleanField


class BSSDLNAEditForm(SanicForm):
    """
    for editing dlna
    """
    enabled = BooleanField('Enabled')

    def __init__(self, *args, **kwargs):
        super(BSSDLNAEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSDLNAEditForm, self).validate()
        if not initial_validation:
            return False
        return True
