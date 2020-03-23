from sanic_wtf import SanicForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class BookAddForm(SanicForm):
    """
    # for adding books
    """
    book_list = TextAreaField('Book ISBN(s)', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(BookAddForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BookAddForm, self).validate()
        if not initial_validation:
            return False
        return True
