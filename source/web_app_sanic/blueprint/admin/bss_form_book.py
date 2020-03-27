from sanic_wtf import SanicForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class BSSBookAddForm(SanicForm):
    """
    # for adding books
    """
    book_list = TextAreaField('Book ISBN(s)', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(BSSBookAddForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSBookAddForm, self).validate()
        if not initial_validation:
            return False
        return True
