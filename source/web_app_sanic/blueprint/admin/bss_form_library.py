from sanic_wtf import SanicForm
from wtforms import StringField


class BSSLibraryAddEditForm(SanicForm):
    """
    for editing the library
    """
    # description = TextAreaField('Description', validators=[DataRequired()])
    library_path = StringField(
        'Library Path')  # , validators=[DataRequired(), Length(min=1, max=255)])  # remove required due to browse buttons

    def __init__(self, *args, **kwargs):
        super(BSSLibraryAddEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSLibraryAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True
