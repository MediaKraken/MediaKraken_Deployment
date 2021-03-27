from sanic_wtf import SanicForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length


# for editing sync jobs
class BSSSyncEditForm(SanicForm):
    # fields
    name = StringField("Name", validators=[DataRequired()])
    target_type = SelectField("Sync Type", choices=[('Local File System', 'Local File System'),
                                                    ("Remote Client", "Remote Client"),
                                                    ("google", "Google Drive"),
                                                    ('dropbox', 'Dropbox'),
                                                    ('onedrive', 'OneDrive'),
                                                    ('awss3', 'AWS S3')])
    target_file_size = SelectField("File Size", choices=[('Clone', 'Clone'),
                                                         ('250MB', '250MB'),
                                                         ('500MB', '500MB'),
                                                         ('1GB', '1GB'),
                                                         ('2GB', '2GB'),
                                                         ('2.5GB', '2.5GB'),
                                                         ('3GB', '3GB'),
                                                         ('4GB', '4GB'),
                                                         ('5GB', '5GB'),
                                                         ('10GB', '10GB'),
                                                         ('25GB', '25GB')])
    target_container = SelectField("Container", choices=[('mkv', 'Matroska (mkv)'),
                                                         ('mp4', 'MPEG-4 (mp4)'),
                                                         ('mpeg', 'MPEG-2'),
                                                         ('avi', 'Audio Video Interleaved (avi)')])
    target_codec = SelectField("Codec", choices=[('h264', 'H.264 AVC'),
                                                 ('hevc', 'H.265 HEVC'),
                                                 ('flv1', 'Flash Video'),
                                                 ('mpeg2video', 'MPEG-2'),
                                                 ('Copy', 'Copy')])
    # flv1     FLV / Sorenson Spark / Sorenson H.263 (Flash Video) (decoders: flv ) (encoders: flv )
    # h264     H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (encoders: libx264 libx264rgb )
    # hevc          H.265 / HEVC (High Efficiency Video Coding) (encoders: libx265 )
    # mpeg2video           MPEG-2 video (decoders: mpeg2video mpegvideo )
    target_audio_channels = SelectField("Audio Channel(s)", choices=[('1.0', '1.0 Mono'),
                                                                     ('2.0', '2.0 Stereo'),
                                                                     ('3.0', '3.0 Surround'),
                                                                     ('5.1', '5.1 Surround'),
                                                                     ('6.1', '6.1 Surround'),
                                                                     ('7.1', '7.1 Surround'),
                                                                     ('Copy', 'Copy')])
    target_audio_codec = SelectField("Audio Codec", choices=[('Copy', 'Copy'),
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
    target_sample_rate = SelectField("Sample Rate", choices=[('Default', 'Default'),
                                                             ('22050', '22,050'),
                                                             ('44100', '44,100 Audio CD'),
                                                             ('96000', '96,000 DVD-Audio'),
                                                             ('192000', 'DVD-Audio'),
                                                             ('2822400', '2,822,400 SACD')])
    target_priority = SelectField("Priority", choices=[('1', 'Low'), ('2', 'Medium'),
                                                       ('3', 'High'), ('4', 'ASAP')])
    target_output_path = StringField("Output File", validators=[DataRequired(),
                                                              Length(min=1, max=255)])

    def __init__(self, *args, **kwargs):
        super(BSSSyncEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSSyncEditForm, self).validate()
        if not initial_validation:
            return False
        return True
