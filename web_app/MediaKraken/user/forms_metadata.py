# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from decimal import ROUND_UP
from .models import User


class MetaMovieEditForm(Form):
    """
    # for editing the movie metadata
    """
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


class MetaAlbumEditForm(Form):
    """
    # for editing the album metadata
    """
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaAlbumEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaAlbumEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class MetaSongEditForm(Form):
    """
    # for editing the song metadata
    """
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


class MetaTVShowEditForm(Form):
    """
    # for editing the tvshow metadata
    """
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class MetaTVShowEpisodeEditForm(Form):
    """
    # for editing the tvshow episode metadata
    """
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEpisodeEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEpisodeEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class MetaGameEditForm(Form):
    """
    # for editing the game metadata
    """
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class MetaGameSystemEditForm(Form):
    """
    # for editing the game system metadata
    """
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEpisodeEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEpisodeEditForm, self).validate()
        if not initial_validation:
            return False
        return True
