from sanic_wtf import SanicForm
from wtforms import StringField


class BSSLinkAddEditForm(SanicForm):
    """
    for editing the link
    """
    link_path = StringField(
        'Link Path')  # , validators=[DataRequired(), Length(min=1, max=255)])  # remove required due to browse buttons

    def __init__(self, *args, **kwargs):
        super(BSSLinkAddEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSLinkAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True
