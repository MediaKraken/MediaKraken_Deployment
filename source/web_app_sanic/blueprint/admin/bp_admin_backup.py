import json
import os

from common import common_database
from common import common_file
from common import common_global
from common import common_network_cloud
from common import common_string
from common import common_pagination_bootstrap
from sanic import Blueprint
from web_app_sanic.blueprint.admin.bss_form_backup import BSSBackupEditForm

blueprint_admin_backup = Blueprint('name_blueprint_admin_backup', url_prefix='/admin')


@blueprint_admin_backup.route("/admin_backup", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_backup.html')
@common_global.auth.login_required
async def url_bp_admin_backup(request):
    """
    List backups from local fs and cloud
    """
    form = BSSBackupEditForm(request)
    errors = {}
    if request.method == 'POST':
        if form.validate_on_submit():
            print('validated', flush=True)
            print(request.form['backup'], flush=True)
            if request.form['backup'] == ['Update Backup']:
                pass
            elif request.form['backup'] == ['Submit Backup']:
                print('startbackup', flush=True)
                common_database.com_database_backup()
                request['flash']("Postgresql Database Backup Task Submitted.", "success")
        else:
            flash_errors(form)
    backup_enabled = False
    backup_files = []
    local_file_backups = common_file.com_file_dir_list(dir_name='/mediakraken/backup',
                                                       filter_text='dump', walk_dir=False,
                                                       skip_junk=False, file_size=True,
                                                       directory_only=False, file_modified=False)
    if local_file_backups is not None:
        for backup_local in local_file_backups:
            backup_files.append((backup_local[0], 'Local',
                                 common_string.com_string_bytes2human(backup_local[1])))
    # TODO
    # # cloud backup list
    # if len(g.option_config_json['Cloud']) > 0:  # to see if the json has been populated
    #     cloud_handle = common_network_cloud.CommonLibCloud(g.option_config_json)
    #     for backup_cloud in cloud_handle.com_net_cloud_list_data_in_container(
    #             g.option_config_json['MediaKrakenServer']['BackupContainerName']):
    #         backup_files.append((backup_cloud.name, backup_cloud.type,
    #                              common_string.com_string_bytes2human(backup_cloud.size)))
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request, user.per_page)
    pagination = Pagination(request,
                            total=len(backup_files),
                            record_name='backups',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'form': form,
        'errors': errors,
        'backup_list': sorted(backup_files, reverse=True),
        'data_interval': ('Hours', 'Days', 'Weekly'),
        'data_class': common_network_cloud.supported_providers,
        'data_enabled': backup_enabled,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_backup.route('/admin_backup_delete', methods=["POST"])
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


@blueprint_admin_backup.route('/admin_backup_restore/<backup_filename>', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_backup_restore(request, backup_filename):
    """
    run restore script on db container
    """
    # since I have to strip the first / as url_for gets mad
    common_database.com_database_restore(backup_filename.replace('*', '/'))
    return json.dumps({'status': 'OK'})
