from bss_form_required_if import RequiredIf
from sanic_wtf import SanicForm as Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


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
    docker_musicbrainz_code = TextField('Brainzcode', validators=[RequiredIf('docker_musicbrainz'),
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
