# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import locale
locale.setlocale(locale.LC_ALL, '')
import pygal
import json
import logging # pylint: disable=W0611
import os
import sys
sys.path.append('..')
from flask import Blueprint, render_template, g, request, current_app, jsonify, flash,\
     url_for, redirect, session, abort
from flask_login import login_required
from flask_paginate import Pagination
blueprint = Blueprint("admins", __name__, url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from functools import partial
from MediaKraken.admins.forms import CronEditForm
from MediaKraken.admins.forms import LibraryAddEditForm
from MediaKraken.admins.forms import ShareAddEditForm
from MediaKraken.admins.forms import BackupEditForm
from MediaKraken.admins.forms import DLNAEditForm
from MediaKraken.admins.forms import UserEditForm
from MediaKraken.admins.forms import AdminSettingsForm

from common import common_config_ini
from common import common_network_cifs
from common import common_cloud
from common import common_file
from common import common_network
from common import common_pagination
from common import common_string
from common import common_system
from common import common_transmission
from common import common_version
from common import common_zfs
import database as database_base


outside_ip = None
option_config_json, db_connection = common_config_ini.com_config_read()


CLOUD_HANDLE = common_cloud.CommonCloud(option_config_json)


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
    data_transmission_active = False
    if g.db_connection.db_opt_status_read()['mm_options_json']['Transmission']['Host'] != None:
        data_transmission_active = True
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
                           data_server_info_server_version=common_version.APP_VERSION,
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
                           data_library=locale.format('%d',\
                               g.db_connection.db_table_count('mm_media_dir'), True),
                           data_share=locale.format('%d',\
                               g.db_connection.db_table_count('mm_media_share'), True),
                           data_transmission_active=data_transmission_active,
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


#@blueprint.route("/dlna")
#@blueprint.route("/dlna/")
#@login_required
#@admin_required
#def admin_dlna():
#    return render_template("admin/admin_dlna.html")


@blueprint.route('/cron')
@blueprint.route('/cron/')
@login_required
@admin_required
def admin_cron_display_all():
    """
    Display cron jobs
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_cron_list_count(False),
                                                  record_name='Cron Jobs',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('admin/admin_cron.html',
                           media_cron=g.db_connection.db_cron_list(False, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/cron_edit/<guid>/', methods=['GET', 'POST'])
@blueprint.route('/cron_edit/<guid>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_cron_edit(guid):
    """
    Edit cron job page
    """
    form = CronEditForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        pass
    return render_template('admin/admin_cron_edit.html', guid=guid, form=form)


@blueprint.route("/tvtuners", methods=["GET", "POST"])
@blueprint.route("/tvtuners/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_tvtuners():
    """
    List tvtuners
    """
    tv_tuners = []
    for row_data in g.db_connection.db_tuner_list():
        tv_tuners.append((row_data['mm_tuner_id'], row_data['mm_tuner_json']['HWModel']\
        + " (" + row_data['mm_tuner_json']['Model'] + ")", row_data['mm_tuner_json']['IP'],\
        row_data['mm_tuner_json']['Active'], len(row_data['mm_tuner_json']['Channels'])))
    return render_template("admin/admin_tvtuners.html", data_tuners=tv_tuners)


@blueprint.route("/nas", methods=["GET", "POST"])
@blueprint.route("/nas/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_nas():
    """
    List all NAS devices
    """
    nas_devices = []
    return render_template("admin/admin_nas.html", data_nas=nas_devices)


@blueprint.route("/transmission")
@blueprint.route("/transmission/")
@login_required
@admin_required
def admin_transmission():
    """
    Display transmission page
    """
    trans_connection = common_transmission.CommonTransmission(option_config_json)
    transmission_data = []
    if trans_connection is not None:
        torrent_no = 1
        for torrent in trans_connection.com_trans_get_torrent_list():
            transmission_data.append((locale.format('%d', torrent_no, True), torrent.name,\
                torrent.hashString, torrent.status, torrent.progress, torrent.ratio))
            torrent_no += 1
    return render_template("admin/admin_transmission.html", data_transmission=transmission_data)


@blueprint.route('/transmission_delete', methods=["POST"])
@login_required
@admin_required
def admin_transmission_delete_page():
    """
    Delete torrent from transmission
    """
    #g.db_connection.db_Audit_Path_Delete(request.form['id'])
    #g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/transmission_edit', methods=["POST"])
@login_required
@admin_required
def admin_transmission_edit_page():
    """
    Edit a torrent from transmission
    """
    #g.db_connection.db_Audit_Path_Delete(request.form['id'])
    #g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route("/library", methods=["GET", "POST"])
@blueprint.route("/library/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_library():
    """
    List all media libraries
    """
    if request.method == 'POST':
        g.db_connection.db_trigger_insert(('python', './subprogram_file_scan.py'))
        flash("Scheduled media scan.")
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_audit_paths_count(),
                                                  record_name='library dir(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template("admin/admin_library.html",
                           media_dir=g.db_connection.db_audit_paths(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route("/library_edit", methods=["GET", "POST"])
@blueprint.route("/library_edit/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_library_edit_page():
    """
    allow user to edit lib
    """
    form = LibraryAddEditForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['action_type'] == 'Add':
                # check for UNC
                if request.form['library_path'][:1] == "\\":
                    addr, share, path = common_string.com_string_unc_to_addr_path(\
                        request.form['library_path'])
                    logging.info('smb info: %s %s %s' % (addr, share, path))
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(addr)
                    if not smb_stuff.com_cifs_share_directory_check(share, path):
                        smb_stuff.com_cifs_close()
                        flash("Invalid UNC path.", 'error')
                        return redirect(url_for('admins.admin_library_edit_page'))
                    smb_stuff.com_cifs_close()
                # smb/cifs mounts
                elif request.form['library_path'][0:3] == "smb":
                    # TODO
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(ip_addr, user_name='guest', user_password='')
                    smb_stuff.com_cifs_share_directory_check(share_name, dir_path)
                    smb_stuff.com_cifs_close()
                # nfs mount
                elif request.form['library_path'][0:3] == "nfs":
                    # TODO
                    pass
                elif not os.path.isdir(request.form['library_path']):
                    flash("Invalid library path.", 'error')
                    return redirect(url_for('admins.admin_library_edit_page'))
                # verify it doesn't exit and add
                if g.db_connection.db_audit_path_check(request.form['library_path']) == 0:
                    g.db_connection.db_audit_path_add(request.form['library_path'],\
                        request.form['Lib_Class'])
                    g.db_connection.db_commit()
                    return redirect(url_for('admins.admin_library'))
                else:
                    flash("Path already in library.", 'error')
                    return redirect(url_for('admins.admin_library_edit_page'))
            elif request.form['action_type'] == 'Browse...': # popup browse form
                pass
            elif request.form['action_type'] == 'Synology': # popup browse form for synology
                pass
        else:
            flash_errors(form)
    class_list = []
    for row_data in g.db_connection.db_media_class_list():
        if row_data[2]: # flagged for display
            class_list.append((row_data[0], row_data[1]))
    return render_template("admin/admin_library_edit.html", form=form,
                           data_class=class_list)


@blueprint.route('/library_delete', methods=["POST"])
@login_required
@admin_required
def admin_library_delete_page():
    """
    Delete library action 'page'
    """
    g.db_connection.db_audit_path_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/getLibraryById', methods=['POST'])
@login_required
@admin_required
def getLibraryById():
    result = g.db_connection.db_audit_path_by_uuid(request.form['id'])
    return json.dumps({'Id': result['mm_media_dir_guid'],\
        'Path': result['mm_media_dir_path'], 'Media Class': result['mm_media_dir_class_type']})


@blueprint.route('/updateLibrary', methods=['POST'])
@login_required
@admin_required
def updateLibrary():
    g.db_connection.db_audit_path_update_by_uuid(request.form['new_path'],\
        request.form['new_class'], request.form['id'])
    return json.dumps({'status': 'OK'})


@blueprint.route("/share", methods=["GET", "POST"])
@blueprint.route("/share/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_share():
    """
    List all share/mounts
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count('mm_media_share'),
                                                  record_name='share(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template("admin/admin_share.html",
                           media_dir=g.db_connection.db_audit_shares(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route("/share_edit", methods=["GET", "POST"])
@blueprint.route("/share_edit/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_share_edit_page():
    """
    allow user to edit share
    """
    form = ShareAddEditForm(request.form)
    logging.info('hereeditshare')
    if request.method == 'POST':
        logging.info('herepost')
        if form.validate_on_submit():
            logging.info('here')
            logging.info(request.form['action_type'])
            if request.form['action_type'] == 'Add':
                # check for UNC
                if request.form['storage_mount_type'] == "unc":
                    addr, share, path = common_string.com_string_unc_to_addr_path(\
                        request.form['share_path'])
                    logging.info('unc info: %s %s %s' % (addr, share, path))
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(addr)
                    if not smb_stuff.com_cifs_share_directory_check(share, path):
                        smb_stuff.com_cifs_close()
                        flash("Invalid UNC path.", 'error')
                        return redirect(url_for('admins.admin_share_edit_page'))
                    smb_stuff.com_cifs_close()

                # smb/cifs mounts
                elif request.form['storage_mount_type'] == "smb":
                    # TODO
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(request.form['storage_mount_server'],\
                        user_name='guest', user_password='')
                    smb_stuff.com_cifs_share_directory_check(share_name,\
                        request.form['share_path'])
                    smb_stuff.com_cifs_close()
                # nfs mount
                elif request.form['storage_mount_type'] == "nfs":
                    # TODO
                    pass
                elif not os.path.isdir(request.form['storage_mount_path']):
                    flash("Invalid share path.", 'error')
                    return redirect(url_for('admins.admin_share_edit_page'))
                # verify it doesn't exit and add
                if g.db_connection.db_audit_share_check(request.form['storage_mount_path']) == 0:
                    g.db_connection.db_audit_share_add(request.form['storage_mount_path'],\
                        request.form['Lib_Class'])
                    g.db_connection.db_commit()
                    return redirect(url_for('admins.admin_share'))

                else:
                    flash("Share already mapped.", 'error')
                    return redirect(url_for('admins.admin_share_edit_page'))
            elif request.form['action_type'] == 'Browse':
                # browse for smb shares on the host network
                pass
        else:
            flash_errors(form)
    return render_template("admin/admin_share_edit.html", form=form)


@blueprint.route('/share_delete', methods=["POST"])
@login_required
@admin_required
def admin_share_delete_page():
    """
    Delete share action 'page'
    """
    g.db_connection.db_audit_share_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/getShareById', methods=['POST'])
@login_required
@admin_required
def getShareById():
    result = g.db_connection.db_audit_share_by_uuid(request.form['id'])
    return json.dumps({'Id': result['mm_share_dir_guid'],\
        'Path': result['mm_share_dir_path']})


@blueprint.route('/updateShare', methods=['POST'])
@login_required
@admin_required
def updateShare():
    g.db_connection.db_audit_share_update_by_uuid(request.form['new_share_type'],\
                                                  request.form['new_share_user'],\
                                                  request.form['new_share_password'],\
                                                  request.form['new_share_server'],\
                                                  request.form['new_share_path'],\
                                                  request.form['id'])
    return json.dumps({'status': 'OK'})


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
        CLOUD_HANDLE.com_cloud_file_delete('awss3', file_path, True)
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
        backup_files.append((backup_local[0], 'Local',\
            common_string.com_string_bytes2human(backup_local[1])))
    # cloud backup list
    for backup_cloud in CLOUD_HANDLE.com_cloud_backup_list():
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
                           data_class=common_cloud.CLOUD_BACKUP_CLASS,
                           data_enabled=backup_enabled,
                           page=page,
                           per_page=per_page,
                           pagination=pagination
                          )


@blueprint.route("/ffmpeg_stat")
@blueprint.route("/ffmpeg_stat/")
@login_required
@admin_required
def ffmpeg_stat():
    return redirect("http://www.example.com/status.html", code=302)  # status.html is ffmpeg page


@blueprint.route("/server_stat")
@blueprint.route("/server_stat/")
@login_required
@admin_required
def admin_server_stat():
    """
    Display server stats via psutils
    """
    return render_template("admin/admin_server_stats.html",
                           data_disk=common_system.com_system_disk_usage_all(True),
                           data_cpu_usage=common_system.com_system_cpu_usage(True),
                           data_mem_usage=common_system.com_system_virtual_memory(None),
                           data_network_io=common_network.mk_network_io_counter())


@blueprint.route("/server_stat_slave")
@blueprint.route("/server_stat_slave/")
@login_required
@admin_required
def admin_server_stat_slave():
    """
    Display stats on connected slaves via psutils
    """
    return render_template("admin/admin_server_stats_slave.html",
                           data_disk=common_system.com_system_disk_usage_all(True),
                           data_cpu_usage=common_system.com_system_cpu_usage(True),
                           data_mem_usage=common_system.com_system_virtual_memory(None))


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


@blueprint.route("/zfs")
@blueprint.route("/zfs/")
@login_required
@admin_required
def admin_server_zfs():
    """
    Display zfs admin page
    """
    return render_template("admin/admin_server_zfs.html",
                           data_zpool=common_zfs.com_zfs_zpool_list())


@blueprint.route("/link_server")
@blueprint.route("/link_server/")
@login_required
@admin_required
def admin_server_link_server():
    """
    Display page for linking server
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_link_list_count(),
                                                  record_name='linked servers',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template("admin/admin_link.html",
                           data=g.db_connection.db_link_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@blueprint.route('/link_delete', methods=["POST"])
@login_required
@admin_required
def admin_link_delete_page():
    """
    Delete linked server action 'page'
    """
    g.db_connection.db_link_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status':'OK'})


@blueprint.route("/cloud_google_drive")
@blueprint.route("/cloud_google_drive/")
@login_required
@admin_required
def admin_cloud_google_drive():
    return render_template("admin/cloud/cloud_google_drive.html")


@blueprint.route("/cloud_onedrive")
@blueprint.route("/cloud_onedrive/")
@login_required
@admin_required
def admin_cloud_onedrive():
    return render_template("admin/cloud/cloud_onedrive.html")


@blueprint.route("/cloud_aws_s3")
@blueprint.route("/cloud_aws_s3/")
@login_required
@admin_required
def admin_cloud_aws_s3():
    return render_template("admin/cloud/cloud_aws_s3.html")


@blueprint.route("/cloud_dropbox")
@blueprint.route("/cloud_dropbox/")
@login_required
@admin_required
def admin_cloud_dropbox():
    return render_template("admin/cloud/cloud_dropbox.html")


@blueprint.route("/chart_browser")
@blueprint.route("/chart_browser/")
@login_required
@admin_required
def admin_chart_browser():
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart = line_chart.render(is_unicode=True)
    return render_template("admin/chart/chart_base_usage.html", line_chart=line_chart)


@blueprint.route("/chart_client_usage")
@blueprint.route("/chart_client_usage/")
@login_required
@admin_required
def admin_chart_client_usage():
    line_chart = pygal.Line()
    line_chart.title = 'Client usage'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Theater', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Roku', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('Web', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('iOS', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.add('Android', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.add('Tizen', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart = line_chart.render(is_unicode=True)
    return render_template("admin/chart/chart_base_usage.html", line_chart=line_chart)


@blueprint.route("/database")
@blueprint.route("/database/")
@login_required
@admin_required
def admin_database_statistics():
    """
    Display database statistics page
    """
    db_stats_count = []
    for row_data in g.db_connection.db_pgsql_row_count():
        db_stats_count.append((row_data[1], locale.format('%d', row_data[2], True)))
    return render_template("admin/admin_server_database_stats.html",
                           data_db_size=g.db_connection.db_pgsql_table_sizes(),
                           data_db_count=db_stats_count)


@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>/list')
@login_required
@admin_required
def admin_listdir(path):
    """
    Local file browser
    """
    def gather_fileinfo(path, ospath, filename):
        osfilepath = os.path.join(ospath, filename)
        if os.path.isdir(osfilepath) and not filename.startswith('.'):
            return {'type': 'd', 'filename': filename,
                    'link': url_for('admins.admin_listdir',
                                    path=os.path.join(path, filename))}
        else:
            return {'type': 'f', 'filename': filename,
                    'fullpath': os.path.join(path, filename)}
    try:
        path = os.path.normpath(path)
        ospath = os.path.join('/', path)
        files = list(map(partial(gather_fileinfo, path, ospath), os.listdir(ospath)))
        files = list(filter(lambda file: file is not None, files))
        files.sort(key=lambda i: (i['type'] == 'file' and '1' or '0') + i['filename'].lower())
        return render_template('admin/admin_fs_browse.html',
                               files=files,
                               parent=os.path.dirname(path),
                               path=path)
    except IOError:
        abort(404)


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception):
    """
    Executes after each request
    """
    g.db_connection.db_close()
