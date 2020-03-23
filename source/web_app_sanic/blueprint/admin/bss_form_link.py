from sanic_wtf import SanicForm
from wtforms import TextField


class LinkAddEditForm(SanicForm):
    """
    for editing the link
    """
    link_path = TextField(
        'Link Path')  # , validators=[DataRequired(), Length(min=1, max=255)])  # remove required due to browse buttons

    def __init__(self, *args, **kwargs):
        super(LinkAddEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LinkAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True
