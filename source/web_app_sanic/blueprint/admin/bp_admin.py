import os

from common import common_global
from common import common_hash
from common import common_internationalization
from common import common_network
from common import common_system
from common import common_version
from sanic import Blueprint

blueprint_admin = Blueprint('name_blueprint_admin', url_prefix='/admin')


@blueprint_admin.route("/")
@common_global.jinja_template.template('bss_admin/bss_admin_home.html')
@common_global.auth.login_required
async def url_bp_admin(request):
    """
    Display main server page
    """
    global outside_ip
    if outside_ip is None:
        outside_ip = common_network.mk_network_get_outside_ip()
    data_messages = 0
    data_server_info_server_name = 'Spoots Media'
    nic_data = []
    for key, value in common_network.mk_network_ip_addr().items():
        nic_data.append(key + ' ' + value[0][1])
    data_alerts_dismissable = []
    data_alerts = []
    # read in the notifications
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_notification_read(db_connection):
        if row_data['mm_notification_dismissable']:  # check for dismissable
            data_alerts_dismissable.append((row_data['mm_notification_guid'],
                                            row_data['mm_notification_text'],
                                            row_data['mm_notification_time']))
        else:
            data_alerts.append((row_data['mm_notification_guid'],
                                row_data['mm_notification_text'],
                                row_data['mm_notification_time']))
    data_transmission_active = False
    if await \
            request.app.db_functions.db_opt_status_read(db_connection)['mm_options_json'][
                'Transmission'][
                'Host'] is not None:
        data_transmission_active = True
    # set the scan info
    data_scan_info = []
    scanning_json = await request.app.db_functions.db_opt_status_read(db_connection)[
        'mm_status_json']
    if 'Status' in scanning_json:
        data_scan_info.append(('System', scanning_json['Status'], scanning_json['Pct']))
    for dir_path in await request.app.db_functions.db_library_path_status(db_connection):
        data_scan_info.append((dir_path[0], dir_path[1]['Status'], dir_path[1]['Pct']))
    if os.environ['SWARMIP'] != 'None':
        mediakraken_ip = os.environ['SWARMIP']
    else:
        mediakraken_ip = os.environ['HOST_IP']
    # TODO pool release
    return {
        'data_user_count': common_internationalization.com_inter_number_format(
            await request.app.db_functions.db_user_count(db_connection)),
        'data_server_info_server_name': data_server_info_server_name,
        'data_host_ip': mediakraken_ip,
        'data_server_info_server_ip': nic_data,
        'data_server_info_server_ip_external': outside_ip,
        'data_server_info_server_version': common_version.APP_VERSION,
        'data_server_uptime': common_system.com_system_uptime(),
        'data_active_streams': common_internationalization.com_inter_number_format(
            0),
        'data_alerts_dismissable': data_alerts_dismissable,
        'data_alerts': data_alerts,
        'data_count_media_files': common_internationalization.com_inter_number_format(
            await request.app.db_functions.db_media_known_count(db_connection)),
        'data_count_matched_media': common_internationalization.com_inter_number_format(
            await request.app.db_functions.db_media_matched_count(db_connection)),
        'data_count_streamed_media': common_internationalization.com_inter_number_format(
            0),
        'data_library': common_internationalization.com_inter_number_format(
            await request.app.db_functions.db_table_count(db_connection, 'mm_media_dir')),
        'data_share': common_internationalization.com_inter_number_format(
            await request.app.db_functions.db_table_count(db_connection, 'mm_media_share')),
        'data_transmission_active': data_transmission_active,
        'data_scan_info': data_scan_info,
        'data_messages': data_messages,
        'data_count_meta_fetch': common_internationalization.com_inter_number_format(
            await request.app.db_functions.db_table_count(db_connection, 'mm_download_que')),
    }


@blueprint_admin.route("/admin_settings", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_admin/bss_admin_settings.html')
@common_global.auth.login_required
async def url_bp_admin_server_settings(request):
    """
    Display server settings page
    """
    async with request.app.db_pool.acquire() as db_connection:
        settings_json = await request.app.db_functions.db_opt_status_read(db_connection)[0]
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
    return {
        'form': AdminSettingsForm(request.form),
        'settings_json': settings_json,
        'mediabrainz_api_key': mediabrainz_api_key,
        'opensubtitles_api_key': opensubtitles_api_key
    }


# @blueprint_admin.route("/admin_sidenav")
# @common_global.jinja_template.template('admin/admin_sidenav.html')
# @common_global.auth.login_required
# async def url_bp_admin_sidenav(request):
#     return {}
