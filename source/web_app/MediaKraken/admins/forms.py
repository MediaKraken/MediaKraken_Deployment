# -*- coding: utf-8 -*-

from decimal import ROUND_UP

from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ShareAddEditForm(Form):
    """
    for editing the shares
    """
    # description = TextAreaField('Description', validators=[DataRequired()])
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


class LinkAddEditForm(Form):
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


class BackupEditForm(Form):
    """
    for editing backups
    """
    enabled = BooleanField('Enabled')

    # interval = SelectField('Interval', choices=[('Hours', 'Hours'),\
    # ('Days', 'Days'), ('Weekly', 'Weekly')])
    # time = DecimalField('Time', places = 2, rounding=ROUND_UP)

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
    servername = TextField('Server Name', validators=[
        DataRequired(), Length(min=3, max=250)])
    servermotd = TextField('Server MOTD', validators=[Length(min=0, max=250)])
    activity_purge_interval = SelectField('Purge Activity Data Older Than',
                                          choices=[('Never', 'Never'), ('1 Day', '1 Day'),
                                                   ('Week', 'Week'), ('Month',
                                                                      'Month'),
                                                   ('Quarter', 'Quarter'), ('6 Months',
                                                                            '6 Months'),
                                                   ('Year', 'Year')])
    user_password_lock = SelectField('Lock account after failed attempts',
                                     choices=[('Never', 'Never'), ('3', '3'), ('5', '5'),
                                              ('10', '10')])
    # language = SelectField('Interval', choices=[('Hours', 'Hours'),
    # ('Days', 'Days'), ('Weekly', 'Weekly')])
    # country = SelectField('Interval', choices=[('Hours', 'Hours'),
    # ('Days', 'Days'), ('Weekly', 'Weekly')])

    metadata_with_media = BooleanField('Metadata with Media')
    metadata_sub_media_down = BooleanField('Download Movie/TV Subtitle')
    metadata_sub_code = TextField('OpenSubtitles Key', validators=[Length(min=0, max=250)])
    # meta_language = SelectField('Interval', choices=[('Hours', 'Hours'),\
    # ('Days', 'Days'), ('Weekly', 'Weekly')])
    metadata_sub_skip_if_audio = BooleanField('Skip subtitle if lang in audio track')
    docker_musicbrainz = BooleanField(
        'Start MusicBrainz (brainzcode required https://lime-technology.com/forums/topic/42909-support-linuxserverio-musicbrainz/)')
    docker_musicbrainz_code = TextField('Brainzcode', validators=[DataRequired(),
                                                                  Length(min=1, max=250)])

    docker_mumble = BooleanField('Start Mumble (chat server)')
    docker_pgadmin = BooleanField('Start PgAdmin (database webgui)')
    docker_portainer = BooleanField('Start Portainer (Docker monitor)')
    docker_smtp = BooleanField('Start SMTP (Mail Server)')
    docker_teamspeak = BooleanField('Start Teamspeak 3 (chat server)')
    docker_transmission = BooleanField('Start Transmission (bittorrent webgui)')
    docker_wireshark = BooleanField('Start Wireshark (network sniffer)')

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
    time = DecimalField('Time', places=2, rounding=ROUND_UP)
    script_path = TextField('Script Path', validators=[
        DataRequired(), Length(min=1, max=255)])

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
    time = DecimalField('Time', places=2, rounding=ROUND_UP)
    script_path = TextField('Script Path', validators=[
        DataRequired(), Length(min=1, max=255)])

    def __init__(self, *args, **kwargs):
        super(TaskEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(TaskEditForm, self).validate()
        if not initial_validation:
            return False
        return True
