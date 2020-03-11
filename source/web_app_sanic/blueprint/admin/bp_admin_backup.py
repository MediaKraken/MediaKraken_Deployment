import json
import os

from common import common_file
from common import common_global
from common import common_network_cloud
from common import common_string
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint
from web_app_sanic.blueprint.admin.forms import BackupEditForm

blueprint_admin_backup = Blueprint('name_blueprint_admin_backup', url_prefix='/admin')


@blueprint_admin_backup.route("/backup", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_backup.html')
@common_global.auth.login_required
async def url_bp_admin_backup(request):
    """
    List backups from local fs and cloud
    """
    form = BackupEditForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['backup'] == 'Update':
                pass
            elif request.form['backup'] == 'Start Backup':
                g.db_connection.db_trigger_insert(('python3',
                                                   './subprogram_postgresql_backup.py'))  # this commits
                request['flash']("Postgresql Database Backup Task Submitted.", "success")
        else:
            flash_errors(form)
    backup_enabled = False
    backup_files = []
    local_file_backups = common_file.com_file_dir_list('/mediakraken/backup',
                                                       'dump', False, False, True)
    if local_file_backups is not None:
        for backup_local in local_file_backups:
            backup_files.append((backup_local[0], 'Local',
                                 common_string.com_string_bytes2human(backup_local[1])))
    # cloud backup list
    if len(g.option_config_json['Cloud']) > 0:  # to see if the json has been populated
        cloud_handle = common_network_cloud.CommonLibCloud(g.option_config_json)
        for backup_cloud in cloud_handle.com_net_cloud_list_data_in_container(
                g.option_config_json['MediaKrakenServer']['BackupContainerName']):
            backup_files.append((backup_cloud.name, backup_cloud.type,
                                 common_string.com_string_bytes2human(backup_cloud.size)))
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=len(backup_files),
                            record_name='backups',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'form': form,
        'backup_list': sorted(backup_files, reverse=True),
        'data_interval': ('Hours', 'Days', 'Weekly'),
        'data_class': common_network_cloud.supported_providers,
        'data_enabled': backup_enabled,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_backup.route('/backup_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_backup_delete(request):
    """
    Delete backup file action 'page'
    """
    file_path, file_type = request.form['id'].split('|')
    if file_type == "Local":
        os.remove(file_path)
    else:
        pass
        # TODO, do the actual delete
    return json.dumps({'status': 'OK'})
