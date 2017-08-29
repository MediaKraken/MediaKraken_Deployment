# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from decimal import ROUND_UP
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ShareAddEditForm(Form):
    """
    for editing the shares
    """
    #description = TextAreaField('Description', validators=[DataRequired()])
    storage_mount_type = SelectField('Share type',
        choices=[('unc', 'UNC'), ('smb', 'SMB/CIFS'), ('nfs', 'NFS')])
    storage_mount_user = TextField('Share User')
    storage_mount_password = TextField('Share Password')
    storage_mount_server = TextField('Share hostname or IP address')
    storage_mount_path = TextField('Path')


    def __init__(self, *args, **kwargs):
        super(ShareAddEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(ShareAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class BookAddForm(Form):
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


class LibraryAddEditForm(Form):
    """
    for editing the library
    """
    #description = TextAreaField('Description', validators=[DataRequired()])
    library_path = TextField('Library Path') # , validators=[DataRequired(), Length(min=1, max=255)])  # remove required due to browse buttons


    def __init__(self, *args, **kwargs):
        super(LibraryAddEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(LibraryAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class LinkAddEditForm(Form):
    """
    for editing the link
    """
    link_path = TextField('Link Path') # , validators=[DataRequired(), Length(min=1, max=255)])  # remove required due to browse buttons

    def __init__(self, *args, **kwargs):
        super(LinkAddEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(LinkAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class BackupEditForm(Form):
    """
    for editing backups
    """
    enabled = BooleanField('Enabled')
    #interval = SelectField('Interval', choices=[('Hours', 'Hours'),\
    #('Days', 'Days'), ('Weekly', 'Weekly')])
    #time = DecimalField('Time', places = 2, rounding=ROUND_UP)


    def __init__(self, *args, **kwargs):
        super(BackupEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(BackupEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class DLNAEditForm(Form):
    """
    for editing dlna
    """
    enabled = BooleanField('Enabled')


    def __init__(self, *args, **kwargs):
        super(DLNAEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(DLNAEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class UserEditForm(Form):
    """
    for editing user
    """
    username = TextField('Username',
                    validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email',
                    validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                                validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                [DataRequired(), EqualTo('password', message='Passwords must match')])
    enabled = BooleanField('Enabled')
    is_admin = BooleanField('Admin')


    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(UserEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class AdminSettingsForm(Form):
    """
    for editing user
    """
    servername = TextField('Server Name', validators=[DataRequired(), Length(min=3, max=250)])
    servermotd = TextField('Server MOTD', validators=[Length(min=0, max=250)])
    server_bind_addr = TextField('Bind Addr', validators=[Length(min=7, max=15)])
    server_bind_port = TextField('Bind Port', validators=[Length(min=4, max=5)])
    activity_purge_interval = SelectField('Purge Activity Data Older Than',
        choices=[('Never', 'Never'), ('1 Day', '1 Day'), ('Week', 'Week'), ('Month', 'Month'),
        ('Quarter', 'Quarter'), ('6 Months', '6 Months'), ('Year', 'Year')])
    user_password_lock = SelectField('Lock account after failed attempts',
        choices=[('Never', 'Never'), ('3', '3'), ('5', '5'), ('10', '10')])
    metadata_download_metadata = BooleanField('Download Metadata')
    metadata_artwork_metadata = BooleanField('Download Artwork')
    #language = SelectField('Interval', choices=[('Hours', 'Hours'),
    #('Days', 'Days'), ('Weekly', 'Weekly')])
    #country = SelectField('Interval', choices=[('Hours', 'Hours'),
    #('Days', 'Days'), ('Weekly', 'Weekly')])
    metadata_image_bio_person = BooleanField('Download Image/BIO of person(s)')
    metadata_path = TextField('Metadata Path', validators=[DataRequired(), Length(min=1, max=250)])
    metadata_with_media = BooleanField('Metadata with Media')
    metadata_sub_movie_down = BooleanField('Download Movie Subtitle')
    metadata_sub_episode_down = BooleanField('Download TV Subtitle')
    #meta_language = SelectField('Interval', choices=[('Hours', 'Hours'),\
    #('Days', 'Days'), ('Weekly', 'Weekly')])
    metadata_sub_skip_if_audio = BooleanField('Skip subtitle if lang in audio track')
    metadata_source_down_tvmaze = BooleanField('tvmaze')
    metadata_source_down_tmdb = BooleanField('themoviedb')
    metadata_source_down_tvdb = BooleanField('thetvdb')
    metadata_source_down_freedb = BooleanField('FreeDB')
    metadata_source_down_mbrainz = BooleanField('Music Brainz')
    metadata_source_down_anidb = BooleanField('AnimeDB')
    metadata_source_down_chartlyrics = BooleanField('Chart Lyrics')
    metadata_source_down_opensub = BooleanField('OpenSubtitles')
    metadata_source_down_pitchfork = BooleanField('pitchfork')
    metadata_source_down_imvdb = BooleanField('imvdb')
    metadata_source_down_omdb = BooleanField('omdb')
    metadata_source_down_netflixroulette = BooleanField('netflixroulette')
    metadata_sync_path = TextField('Metadata Sync Path',
        validators=[DataRequired(), Length(min=1, max=250)])


    def __init__(self, *args, **kwargs):
        super(AdminSettingsForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(AdminSettingsForm, self).validate()
        if not initial_validation:
            return False
        return True


class CronEditForm(Form):
    """
    for editing the cron jobs
    """
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    enabled = BooleanField('Enabled')
    interval = SelectField('Interval', choices=[('Minutes', 'Minutes'), ('Hours', 'Hours'),
        ('Days', 'Days'), ('Weekly', 'Weekly')])
    time = DecimalField('Time', places = 2, rounding=ROUND_UP)
    script_path = TextField('Script Path', validators=[DataRequired(), Length(min=1, max=255)])


    def __init__(self, *args, **kwargs):
        super(CronEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(CronEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class ChromecastEditForm(Form):
    """
    for editing the chromecast devices
    """
    name = TextField('Name', validators=[DataRequired()])
    ipaddr = TextField('IP Address', validators=[DataRequired()])
    enabled = BooleanField('Enabled')


    def __init__(self, *args, **kwargs):
        super(ChromecastEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(ChromecastEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class TVTunerEditForm(Form):
    """
    for editing the tvtuner devices
    """
    name = TextField('Name', validators=[DataRequired()])
    ipaddr = TextField('IP Address', validators=[DataRequired()])
    enabled = BooleanField('Enabled')


    def __init__(self, *args, **kwargs):
        super(TVTunerEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(TVTunerEditForm, self).validate()
        if not initial_validation:
            return False
        return True


class TaskEditForm(Form):
    """
    for editing the task jobs
    """
    name = TextField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    enabled = BooleanField('Enabled')
    interval = SelectField('Interval', choices=[('Minutes', 'Minutes'), ('Hours', 'Hours'),
        ('Days', 'Days'), ('Weekly', 'Weekly')])
    time = DecimalField('Time', places = 2, rounding=ROUND_UP)
    script_path = TextField('Script Path', validators=[DataRequired(), Length(min=1, max=255)])


    def __init__(self, *args, **kwargs):
        super(TaskEditForm, self).__init__(*args, **kwargs)


    def validate(self):
        initial_validation = super(TaskEditForm, self).validate()
        if not initial_validation:
            return False
        return True
