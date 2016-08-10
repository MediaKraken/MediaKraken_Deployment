# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from decimal import ROUND_UP
from models import User

# for editing the movie metadata
class MetaMovieEditForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    alt_name = TextField('Alternate Name', validators=[DataRequired()])
    overview = TextAreaField('Overview', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaMovieEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaMovieEditForm, self).validate()
        if not initial_validation:
            return False
        return True

# for editing the album metadata
class MetaAlbumEditForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaAlbumEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaAlbumEditForm, self).validate()
        if not initial_validation:
            return False
        return True

# for editing the song metadata
class MetaSongEditForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    lyrics = TextAreaField('Lyrics', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaSongEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaSongEditForm, self).validate()
        if not initial_validation:
            return False
        return True

# for editing the tvshow metadata
class MetaTVShowEditForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEditForm, self).validate()
        if not initial_validation:
            return False
        return True

# for editing the tvshow episode metadata
class MetaTVShowEpisodeEditForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEpisodeEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEpisodeEditForm, self).validate()
        if not initial_validation:
            return False
        return True

# for editing the game metadata
class MetaGameEditForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEditForm, self).validate()
        if not initial_validation:
            return False
        return True

# for editing the game system metadata
class MetaGameSystemEditForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEpisodeEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEpisodeEditForm, self).validate()
        if not initial_validation:
            return False
        return True
