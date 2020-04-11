from common import common_global
from common import common_hash
from sanic import Blueprint
from web_app_sanic.blueprint.admin.bss_form_server_settings import BSSAdminSettingsForm

blueprint_admin_settings = Blueprint('name_blueprint_admin_settings', url_prefix='/admin')


@blueprint_admin_settings.route("/admin_settings", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_admin/bss_admin_settings.html')
@common_global.auth.login_required
async def url_bp_admin_settings(request):
    """
    Display server settings page
    """
    db_connection = await request.app.db_pool.acquire()
    settings_json = await request.app.db_functions.db_opt_json_read(db_connection)
    # setup the crypto
    data = common_hash.CommonHashCrypto()
    mediabrainz_api_key = None
    opensubtitles_api_key = None
    if request.method == 'GET':
        if settings_json['API']['musicbrainz'] is not None:
            mediabrainz_api_key = data.com_hash_gen_crypt_decode(
                settings_json['API']['musicbrainz'])
        if settings_json['API']['opensubtitles'] is not None:
            opensubtitles_api_key = data.com_hash_gen_crypt_decode(
                settings_json['API']['opensubtitles'])
    elif request.method == 'POST':
        # api info
        if request.form['docker_musicbrainz_code']:
            settings_json['API']['musicbrainz'] = data.com_hash_gen_crypt_encode(
                request.form['docker_musicbrainz_code'])
        else:
            settings_json['API']['musicbrainz'] = None
        settings_json['API']['opensubtitles'] = data.com_hash_gen_crypt_encode(
            request.form['metadata_sub_code'])
        # Docker instances info
        settings_json['Docker Instances']['mumble'] = request.form['docker_mumble']
        settings_json['Docker Instances']['musicbrainz'] = request.form['docker_musicbrainz']
        settings_json['Docker Instances']['pgadmin'] = request.form['docker_pgadmin']
        settings_json['Docker Instances']['portainer'] = request.form['docker_portainer']
        settings_json['Docker Instances']['smtp'] = request.form['docker_smtp']
        settings_json['Docker Instances']['teamspeak'] = request.form['docker_teamspeak']
        settings_json['Docker Instances']['transmission'] = request.form['docker_transmission']
        settings_json['Docker Instances']['wireshark'] = request.form['docker_wireshark']
        # main server info
        settings_json['MediaKrakenServer']['Server Name'] = request.form['servername']
        settings_json['MediaKrakenServer']['MOTD'] = request.form['servermotd']
        # save updated info
        await request.app.db_functions.db_opt_update(db_connection, settings_json)
    '''
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
    metadata_sub_down = BooleanField('Download Media Subtitle')
    # meta_language = SelectField('Interval', choices=[('Hours', 'Hours'),\
    # ('Days', 'Days'), ('Weekly', 'Weekly')])
    metadata_sub_skip_if_audio = BooleanField('Skip subtitle if lang in audio track')
    docker_musicbrainz_code = TextField('Brainzcode', validators=[DataRequired(),
                                                                  Length(min=1, max=250)])
    '''
    await request.app.db_pool.release(db_connection)
    return {
        'form': BSSAdminSettingsForm(request),
        'settings_json': settings_json,
        'mediabrainz_api_key': mediabrainz_api_key,
        'opensubtitles_api_key': opensubtitles_api_key
    }
