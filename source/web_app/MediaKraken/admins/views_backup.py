# -*- coding: utf-8 -*-

import json
import os
import sys

sys.path.append('..')
from flask import Blueprint, render_template, g, request, flash
from flask_login import login_required

blueprint = Blueprint("admins_backup", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from MediaKraken.utils import flash_errors
from functools import wraps
from MediaKraken.admins.forms import BackupEditForm
from common import common_network_cloud
from common import common_file
from common import common_global
from common import common_pagination
from common import common_string
import database as database_base


def admin_required(fn):
    """
    Admin check
    """

    @wraps(fn)
    @login_required
    def decorated_view(*args, **kwargs):
        common_global.es_inst.com_elastic_index('info', {"admin access attempt by":
                                                             current_user.get_id()})
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route('/backup_delete', methods=["POST"])
@login_required
@admin_required
def admin_backup_delete_page():
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


@blueprint.route("/backup", methods=["GET", "POST"])
@login_required
@admin_required
def admin_backup():
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
                flash("Postgresql Database Backup Task Submitted.")
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
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=len(backup_files),
                                                  record_name='backups',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("admin/admin_backup.html", form=form,
                           backup_list=sorted(backup_files, reverse=True),
                           data_interval=('Hours', 'Days', 'Weekly'),
                           data_class=common_network_cloud.supported_providers,
                           data_enabled=backup_enabled,
                           page=page,
                           per_page=per_page,
                           pagination=pagination
                           )


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.option_config_json = g.db_connection.db_opt_status_read()[0]
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception):
    """
    Executes after each request
    """
    g.db_connection.db_close()
