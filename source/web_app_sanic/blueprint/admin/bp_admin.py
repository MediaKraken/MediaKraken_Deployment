import json
import os

from common import common_global
from common import common_internationalization
from common import common_network
from common import common_system
from common import common_version
from sanic import Blueprint

blueprint_admin = Blueprint('name_blueprint_admin', url_prefix='/admin')

outside_ip = None


@blueprint_admin.route("/admin_home")
@common_global.jinja_template.template('bss_admin/bss_admin_home.html')
@common_global.auth.login_required
async def url_bp_admin(request):
    """
    Display main server page
    """
    global outside_ip
    if outside_ip is None:
        outside_ip = common_network.mk_network_get_outside_ip()
    data_server_info_server_name = 'Spoots Media'
    nic_data = []
    for key, value in common_network.mk_network_ip_addr().items():
        nic_data.append(key + ' ' + value[0][1])
    data_alerts_dismissable = []
    data_alerts = []
    # read in the notifications
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_notification_read(
            db_connection=db_connection):
        if row_data['mm_notification_dismissable']:  # check for dismissable
            data_alerts_dismissable.append((row_data['mm_notification_guid'],
                                            row_data['mm_notification_text'],
                                            row_data['mm_notification_time']))
        else:
            data_alerts.append((row_data['mm_notification_guid'],
                                row_data['mm_notification_text'],
                                row_data['mm_notification_time']))
    data_transmission_active = False
    row_data = json.loads(
        await request.app.db_functions.db_opt_json_read(db_connection=db_connection))
    if row_data['Docker Instances']['transmission'] is True:
        data_transmission_active = True
    # set the scan info
    data_scan_info = []
    scanning_json = json.loads(
        await request.app.db_functions.db_status_json_read(db_connection=db_connection))
    if 'Status' in scanning_json:
        data_scan_info.append(('System', scanning_json['Status'], scanning_json['Pct']))
    for row_data in await request.app.db_functions.db_library_path_status(
            db_connection=db_connection):
        data_scan_info.append((row_data['mm_media_dir_path'],
                               row_data['mm_media_dir_status']['Status'],
                               row_data['mm_media_dir_status']['Pct']))
    if os.environ['SWARMIP'] != 'None':
        mediakraken_ip = os.environ['SWARMIP']
    else:
        mediakraken_ip = os.environ['HOST_IP']
    user_count = common_internationalization.com_inter_number_format(
        await request.app.db_functions.db_user_count(db_connection=db_connection))
    media_file_count = common_internationalization.com_inter_number_format(
        await request.app.db_functions.db_media_known_count(db_connection=db_connection))
    media_matched_count = common_internationalization.com_inter_number_format(
        await request.app.db_functions.db_media_matched_count(db_connection=db_connection))
    media_library_count = common_internationalization.com_inter_number_format(
        await request.app.db_functions.db_table_count(table_name='mm_media_dir',
                                                      db_connection=db_connection))
    metadata_to_fetch = common_internationalization.com_inter_number_format(
        await request.app.db_functions.db_table_count(table_name='mm_download_que',
                                                      db_connection=db_connection))
    await request.app.db_pool.release(db_connection)
    return {
        'data_user_count': user_count,
        'data_server_info_server_name': data_server_info_server_name,
        'data_host_ip': mediakraken_ip,
        'data_server_info_server_ip': nic_data,
        'data_server_info_server_ip_external': outside_ip,
        'data_server_info_server_version': common_version.APP_VERSION,
        'data_server_uptime': common_system.com_system_uptime(),
        'data_active_streams': common_internationalization.com_inter_number_format(0),
        'data_alerts_dismissable': data_alerts_dismissable,
        'data_alerts': data_alerts,
        'data_count_media_files': media_file_count,
        'data_count_matched_media': media_matched_count,
        'data_count_streamed_media': common_internationalization.com_inter_number_format(0),
        'data_library': media_library_count,
        'data_transmission_active': data_transmission_active,
        'data_scan_info': data_scan_info,
        'data_count_meta_fetch': metadata_to_fetch,
    }

# @blueprint_admin.route("/admin_sidenav")
# @common_global.jinja_template.template('admin/admin_sidenav.html')
# @common_global.auth.login_required
# async def url_bp_admin_sidenav(request):
#     return {}
