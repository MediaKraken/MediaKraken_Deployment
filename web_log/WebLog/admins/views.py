# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify, flash,\
     url_for, redirect, session
from flask_login import login_required
from flask_paginate import Pagination
blueprint = Blueprint("admins", __name__, url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from WebLog.admins.forms import BackupEditForm
from WebLog.admins.forms import UserEditForm
from WebLog.admins.forms import AdminSettingsForm

import pygal
import json
import logging # pylint: disable=W0611
import subprocess
import platform
import os
import sys
sys.path.append('..')
from common import common_config_ini
from common import common_network_cifs
from common import common_cloud
from common import common_file
from common import common_network
from common import common_pagination
from common import common_string
from common import common_system
import database as database_base


import locale
locale.setlocale(locale.LC_ALL, '')

outside_ip = None
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


def flash_errors(form):
    """
    Display errors from list
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


def admin_required(fn):
    """
    Admin check
    """
    @wraps(fn)
    @login_required
    def decorated_view(*args, **kwargs):
        logging.info("admin access attempt by %s" % current_user.get_id())
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)
    return decorated_view


@blueprint.route("/")
@login_required
@admin_required
def admins():
    """
    Display main server page
    """
    global outside_ip
    if outside_ip is None:
        outside_ip = common_network.mk_network_get_outside_ip()
    data_messages = 0
    data_server_info_server_name = 'Spoots Media'
    nic_data = []
    for key, value in common_network.mk_network_ip_addr().iteritems():
        nic_data.append(key + ' ' + value[0][1])
    data_alerts_dismissable = []
    data_alerts = []
    # read in the notifications
    for row_data in g.db_connection.db_notification_read():
        if row_data['mm_notification_dismissable']: # check for dismissable
            data_alerts_dismissable.append((row_data['mm_notification_guid'],\
                row_data['mm_notification_text'], row_data['mm_notification_time']))
        else:
            data_alerts.append((row_data['mm_notification_guid'],\
                row_data['mm_notification_text'], row_data['mm_notification_time']))
    # set the scan info
    data_scan_info = []
    scanning_json = g.db_connection.db_opt_status_read()['mm_status_json']
    if 'Status' in scanning_json:
        data_scan_info.append(('System', scanning_json['Status'], scanning_json['Pct']))
    for dir_path in g.db_connection.db_audit_path_status():
        data_scan_info.append((dir_path[0], dir_path[1]['Status'], dir_path[1]['Pct']))
    return render_template("admin/admins.html",
                           data_user_count=locale.format('%d',\
                               g.db_connection.db_user_list_name_count(), True),
                           data_server_info_server_name=data_server_info_server_name,
                           data_server_info_server_ip=nic_data,
                           data_server_info_server_port\
                               =option_config_json['MediaKrakenServer']['ListenPort'],
                           data_server_info_server_ip_external=outside_ip,
                           data_server_info_server_version='0.1.6',
                           data_server_uptime=common_system.com_system_uptime(),
                           data_active_streams=locale.format('%d', 0, True),
                           data_alerts_dismissable=data_alerts_dismissable,
                           data_alerts=data_alerts,
                           data_count_media_files=locale.format('%d',\
                               g.db_connection.db_known_media_count(), True),
                           data_count_matched_media=locale.format('%d',\
                               g.db_connection.db_matched_media_count(), True),
                           data_count_streamed_media=locale.format('%d', 0, True),
                           data_zfs_active=common_zfs.com_zfs_available(),
                           data_library=locale.format('%d', g.db_connection.db_audit_paths_count(), True),
                           data_scan_info=data_scan_info,
                           data_messages=data_messages
                          )


@blueprint.route("/users")
@blueprint.route("/users/")
@login_required
@admin_required
def admin_users():
    """
    Display user list
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db_connection.db_user_list_name_count(),
                                record_name='users',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('admin/admin_users.html',
                           users=g.db_connection.db_user_list_name(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route("/user_detail/<guid>/")
@blueprint.route("/user_detail/<guid>")
@login_required
@admin_required
def admin_user_detail(guid):
    """
    Display user details
    """
    return render_template('admin/admin_user_detail.html',\
        data_user=g.db_connection.db_user_detail(guid))


@blueprint.route('/user_delete', methods=["POST"])
@login_required
@admin_required
def admin_user_delete_page():
    """
    Delete user action 'page'
    """
    g.db_connection.db_user_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


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
    elif file_type == "AWS" or file_type == "AWS S3":
        common_cloud.com_cloud_File_Delete('awss3', file_path, True)
    return json.dumps({'status': 'OK'})


@blueprint.route("/backup", methods=["GET", "POST"])
@blueprint.route("/backup/", methods=["GET", "POST"])
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
                g.db_connection.db_trigger_insert(('python',\
                    './subprogram_postgresql_backup.py')) # this commits
                flash("Postgresql Database Backup Task Submitted.")
        else:
            flash_errors(form)
    backup_enabled = False
    backup_files = []
    for backup_local in common_file.com_file_dir_list(\
            option_config_json['MediaKrakenServer']['BackupLocal'], 'dump', False, False, True):
        backup_files.append((backup_local[0], 'Local', common_string.com_string_bytes2human(backup_local[1])))
    # cloud backup list
    for backup_cloud in common_cloud.com_cloud_backup_list():
        backup_files.append((backup_cloud.name, backup_cloud.type,\
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
                           data_class=common_cloud.cloud_backup_class,
                           data_enabled=backup_enabled,
                           page=page,
                           per_page=per_page,
                           pagination=pagination
                          )


@blueprint.route("/settings")
@blueprint.route("/settings/")
@login_required
@admin_required
def admin_server_settings():
    """
    Display server settings page
    """
    return render_template("admin/admin_server_settings.html",
                           form=AdminSettingsForm(request.form))


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
        config_handle.get('DB Connections', 'PostDBPort').strip(),\
        config_handle.get('DB Connections', 'PostDBName').strip(),\
        config_handle.get('DB Connections', 'PostDBUser').strip(),\
        config_handle.get('DB Connections', 'PostDBPass').strip())


@blueprint.teardown_request
def teardown_request(exception):
    """
    Executes after each request
    """
    g.db_connection.db_close()
