from sanic_wtf import SanicForm
from wtforms import TextField


class LibraryAddEditForm(SanicForm):
    """
    for editing the library
    """
    # description = TextAreaField('Description', validators=[DataRequired()])
    library_path = TextField(
        'Library Path')  # , validators=[DataRequired(), Length(min=1, max=255)])  # remove required due to browse buttons

    def __init__(self, *args, **kwargs):
        super(LibraryAddEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LibraryAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True