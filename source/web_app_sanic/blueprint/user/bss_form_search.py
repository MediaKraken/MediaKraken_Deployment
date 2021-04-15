from sanic_wtf import SanicForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


# for searching
class BSSSearchEditForm(SanicForm):
    # fields
    search_string = StringField("Search string", validators=[DataRequired()])
    search_media_type = SelectField("Media Type", choices=[('any', 'Any'),
                                                           ('video', 'Video'),
                                                           ('audio', 'Audio'),
                                                           ('image', 'Image'),
                                                           ('publication', 'Publication'),
                                                           ('game', 'Game')])
    # TODO populate from all lang found on media?
    search_primary_language = SelectField("Language", choices=[('any', 'Any'),
                                                               ('sd', 'SD'),
                                                               ('hd', 'HD'),
                                                               ('uhd', 'UHD')])
    # TODO populate from all subtitle lang found on media?
    search_secondary_language = SelectField("Subtitle", choices=[('any', 'Any'),
                                                                 ('sd', 'SD'),
                                                                 ('hd', 'HD'),
                                                                 ('uhd', 'UHD')])
    search_resolution = SelectField("Resolution", choices=[('any', 'Any'),
                                                           ('sd', 'SD'),
                                                           ('hd', 'HD'),
                                                           ('uhd', 'UHD')])
    search_audio_channels = SelectField("Audio Channel(s)", choices=[('any', 'Any'),
                                                                     ('1.0', '1.0 Mono'),
                                                                     ('2.0', '2.0 Stereo'),
                                                                     ('3.0', '3.0 Surround'),
                                                                     ('5.1', '5.1 Surround'),
                                                                     ('6.1', '6.1 Surround'),
                                                                     ('7.1', '7.1 Surround')])
    search_audio_codec = SelectField("Audio Codec", choices=[('any', 'Any'),
                                                             ('aac', 'AAC (Advanced Audio Coding)'),
                                                             ('ac3', 'ATSC A/52A (AC-3)'),
                                                             (
                                                                 'dts',
                                                                 'DCA (DTS Coherent Acoustics)'),
                                                             ('flac', 'FLAC'),
                                                             ('mp3', 'MP3'),
                                                             ('opus', 'Opus'),
                                                             ('truehd', 'TrueHD'),
                                                             ('vorbis', 'Vorbis')])

    def __init__(self, *args, **kwargs):
        super(BSSSearchEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSSearchEditForm, self).validate()
        if not initial_validation:
            return False
        return True
