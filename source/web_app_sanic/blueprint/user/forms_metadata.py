# -*- coding: utf-8 -*-

from sanic_wtf import SanicForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class MetaMovieEditForm(Form):
    """
    # for editing the movie metadata
    """
    name = StringField('Name', validators=[DataRequired()])
    alt_name = StringField('Alternate Name', validators=[DataRequired()])
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
    name = StringField('Name', validators=[DataRequired()])
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
    name = StringField('Name', validators=[DataRequired()])
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
    name = StringField('Name', validators=[DataRequired()])
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
    name = StringField('Name', validators=[DataRequired()])
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
    name = StringField('Name', validators=[DataRequired()])
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
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MetaTVShowEpisodeEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(MetaTVShowEpisodeEditForm, self).validate()
        if not initial_validation:
            return False
        return True
