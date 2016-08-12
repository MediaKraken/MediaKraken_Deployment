# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify, flash, url_for, redirect, session
from flask_login import login_required
from flask_paginate import Pagination
blueprint = Blueprint("admins", __name__, url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from MediaKraken.admins.forms import CronEditForm
from MediaKraken.admins.forms import LibraryAddEditForm
from MediaKraken.admins.forms import BackupEditForm
from MediaKraken.admins.forms import DLNAEditForm
from MediaKraken.admins.forms import UserEditForm
from MediaKraken.admins.forms import AdminSettingsForm

# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("../MediaKraken.ini")

import pygal
import json
import logging
import subprocess
import platform
import os
import sys
sys.path.append('../')
import database as database_base
sys.path.append('../../MediaKraken_Common')
from common import common_cifs
from common import common_cloud
from common import common_file
from common import common_network
from common import common_pagination
from common import common_string
from common import common_system
from common import common_transmission
from common import common_zfs

# import localization
import locale
locale.setlocale(locale.LC_ALL, '')

outside_ip = None

# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("../MediaKraken.ini")


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


def admin_required(fn):
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
    global outside_ip
    if outside_ip is None:
        outside_ip = common_network.MK_Network_Get_Outside_IP()
    data_messages = 0
    data_server_info_server_name = 'Spoots Media'
    nic_data = []
    for key, value in common_network.MK_Network_IP_Addr().iteritems():
        nic_data.append(key + ' ' + value[0][1])
    data_alerts_dismissable = []
    data_alerts = []
    # read in the notifications
    for row_data in g.db.srv_db_Notification_Read():
        if row_data['mm_notification_dismissable']: # check for dismissable
            data_alerts_dismissable.append((row_data['mm_notification_guid'],\
                row_data['mm_notification_text'],row_data['mm_notification_time']))
        else:
            data_alerts.append((row_data['mm_notification_guid'],\
                row_data['mm_notification_text'],row_data['mm_notification_time']))
    # TODO temp
    data_transmission_active = True
    # set the scan info
    data_scan_info = []
    scanning_json = g.db.srv_db_Option_Status_Read()['mm_status_json']
    if 'Status' in scanning_json:
        data_scan_info.append(('System', scanning_json['Status'], scanning_json['Pct']))
    for dir_path in g.db.srv_db_Audit_Path_Status():
        data_scan_info.append((dir_path[0], dir_path[1]['Status'], dir_path[1]['Pct']))
    return render_template("admin/admins.html", 
                           data_user_count = locale.format('%d', g.db.srv_db_User_List_Name_Count(), True),
                           data_server_info_server_name = data_server_info_server_name,
                           data_server_info_server_ip = nic_data,
                           data_server_info_server_port = Config.get('MediaKrakenServer','ListenPort').strip(),
                           data_server_info_server_ip_external = outside_ip,
                           data_server_info_server_version = '0.1.4',
                           data_server_uptime = common_system.common_system_Uptime(),
                           data_active_streams = locale.format('%d', 0, True),
                           data_alerts_dismissable = data_alerts_dismissable,
                           data_alerts = data_alerts,
                           data_count_media_files = locale.format('%d', g.db.srv_db_Known_Media_Count(), True),
                           data_count_matched_media = locale.format('%d', g.db.srv_db_Matched_Media_Count(), True),
                           data_count_streamed_media = locale.format('%d', 0, True),
                           data_zfs_active = common_zfs.common_zfs_Available(),
                           data_library = locale.format('%d', g.db.srv_db_Audit_Paths_Count(), True),
                           data_transmission_active = data_transmission_active,
                           data_scan_info = data_scan_info,
                           data_messages = data_messages
                           )


@blueprint.route("/users")
@blueprint.route("/users/")
@login_required
@admin_required
def admin_users():
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.srv_db_User_List_Name_Count(),
                                record_name='users',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('admin/admin_users.html',
                           users=g.db.srv_db_User_List_Name(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route("/user_detail/<guid>/")
@blueprint.route("/user_detail/<guid>")
@login_required
@admin_required
def admin_user_detail(guid):
    return render_template('admin/admin_user_detail.html',\
        data_user=g.db.srv_db_User_Detail(guid))


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
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.srv_db_Cron_List_Count(False),
                                record_name='Cron Jobs',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('admin/admin_cron.html',
                           media_cron=g.db.srv_db_Cron_List(False, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/cron_edit/<guid>/', methods=['GET', 'POST'])
@blueprint.route('/cron_edit/<guid>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_cron_edit(guid):
    form = CronEditForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        pass
    return render_template('admin/admin_cron_edit.html', guid=guid, form=form )


@blueprint.route("/tvtuners", methods=["GET", "POST"])
@blueprint.route("/tvtuners/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_tvtuners():
    tv_tuners = []
    for row_data in g.db.srv_db_Tuner_List():
        tv_tuners.append((row_data['mm_tuner_id'], row_data['mm_tuner_json']['HWModel']\
        + " (" + row_data['mm_tuner_json']['Model'] + ")", row_data['mm_tuner_json']['IP'],\
        row_data['mm_tuner_json']['Active'], len(row_data['mm_tuner_json']['Channels'])))
    return render_template("admin/admin_tvtuners.html", data_tuners = tv_tuners)


@blueprint.route("/nas", methods=["GET", "POST"])
@blueprint.route("/nas/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_nas():
    nas_devices = []
    return render_template("admin/admin_nas.html", data_nas = nas_devices)


@blueprint.route("/transmission")
@blueprint.route("/transmission/")
@login_required
@admin_required
def admin_transmission():
    trans_connection = common_transmission.common_transmission_API()
    transmission_data = []
    if trans_connection is not None:
        torrent_no = 1
        for torrent in trans_connection.common_transmission_Get_Torrent_List():
            transmission_data.append((locale.format('%d', torrent_no, True), torrent.name,\
                torrent.hashString, torrent.status, torrent.progress, torrent.ratio))
            torrent_no += 1
    return render_template("admin/admin_transmission.html", data_transmission=transmission_data)


@blueprint.route('/transmission_delete',methods=["POST"])
@login_required
@admin_required
def admin_transmission_delete_page():
    #g.db.srv_db_Audit_Path_Delete(request.form['id'])
    #g.db.srv_db_Commit()
    return json.dumps({'status':'OK'})


@blueprint.route('/transmission_edit',methods=["POST"])
@login_required
@admin_required
def admin_transmission_edit_page():
    #g.db.srv_db_Audit_Path_Delete(request.form['id'])
    #g.db.srv_db_Commit()
    return json.dumps({'status':'OK'})


@blueprint.route("/library", methods=["GET", "POST"])
@blueprint.route("/library/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_library():
    if request.method == 'POST':
        g.db.srv_db_Trigger_Insert(('python', './subprogram/subprogram_file_scan.py'))
        flash("Scheduled media scan.")
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.srv_db_Audit_Paths_Count(),
                                record_name='library dir(s)',
                                format_total=True,
                                format_number=True,
                                )
    return render_template("admin/admin_library.html",
                           media_dir=g.db.srv_db_Audit_Paths(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route("/library_edit", methods=["GET", "POST"])
@blueprint.route("/library_edit/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_library_edit_page():
    form = LibraryAddEditForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['action_type'] == 'Add':
                # check for UNC
                if request.form['library_path'][:1] == "\\":
                    addr, share, path = common_string.UNC_To_Addr_Share_Path(request.form['library_path'])
                    smb_stuff = common_cifs.common_cifs_Share_API()
                    smb_stuff.common_cifs_Connect(addr)
                    if not smb_stuff.common_cifs_Share_Directory_Check(share, path):
                        smb_stuff.common_cifs_Close()
                        flash("Invalid UNC path.", 'error')
                        return redirect(url_for('admins.admin_library_edit_page'))                      
                    smb_stuff.common_cifs_Close()
                elif request.form['library_path'][0:3] == "smb":
                    # TODO                    
                    smb_stuff = common_cifs.common_cifs_Share_API()
                    smb_stuff.common_cifs_Connect(ip_addr, user_name='guest', user_password='')
                    smb_stuff.common_cifs_Share_Directory_Check(share_name, dir_path)
                    smb_stuff.common_cifs_Close()
                elif not os.path.isdir(request.form['library_path']):
                    flash("Invalid library path.", 'error')
                    return redirect(url_for('admins.admin_library_edit_page'))
                # verify it doesn't exit and add
                if g.db.srv_db_Audit_Path_Check(request.form['library_path']) == 0:
                    g.db.srv_db_Audit_Path_Add(request.form['library_path'],request.form['Lib_Class'])
                    g.db.srv_db_Commit()
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
    for row_data in g.db.srv_db_Media_Class_List():
        if row_data[2]: # flagged for display
            class_list.append((row_data[0], row_data[1]))
    return render_template("admin/admin_library_edit.html", form=form,
                           data_class = class_list)


@blueprint.route('/library_delete',methods=["POST"])
@login_required
@admin_required
def admin_library_delete_page():
    g.db.srv_db_Audit_Path_Delete(request.form['id'])
    g.db.srv_db_Commit()
    return json.dumps({'status':'OK'})


@blueprint.route('/getLibraryById',methods=['POST'])
@login_required
@admin_required
def getLibraryById():
    result = g.db.srv_db_Audit_Path_By_UUID(request.form['id'])
    return json.dumps({'Id': result['mm_media_dir_guid'],\
        'Path': result['mm_media_dir_path'],'Media Class': result['mm_media_dir_class_type']})


@blueprint.route('/updateLibrary', methods=['POST'])
@login_required
@admin_required
def updateLibrary():
    g.db.srv_db_Audit_Path_Update_By_UUID(request.form['new_path'],\
        request.form['new_class'], request.form['id'])
    return json.dumps({'status':'OK'})


@blueprint.route('/user_delete',methods=["POST"])
@login_required
@admin_required
def admin_user_delete_page():
    g.db.srv_db_User_Delete(request.form['id'])
    g.db.srv_db_Commit()
    return json.dumps({'status':'OK'})


@blueprint.route('/backup_delete',methods=["POST"])
@login_required
@admin_required
def admin_backup_delete_page():
    file_path, file_type = request.form['id'].split('|')
    if file_type == "Local":
        os.remove(file_path)
    elif file_type == "AWS" or file_type == "AWS S3":
        common_cloud.common_cloud_File_Delete('awss3', file_path, True)
    return json.dumps({'status':'OK'})


@blueprint.route("/backup", methods=["GET", "POST"])
@blueprint.route("/backup/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_backup():
    form = BackupEditForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['backup'] == 'Update':
                pass
            elif request.form['backup'] == 'Start Backup':
                g.db.srv_db_Trigger_Insert(('python',\
                    './subprogram/subprogram_postgresql_backup.py')) # this commits
                flash("Postgresql Database Backup Task Submitted.")
        else:
            flash_errors(form)
    backup_enabled = False
    backup_files = []
    for backup_local in common_file.common_file_Dir_List(Config.get('MediaKrakenServer','BackupLocal').strip(), 'dump', False, False, True):
        backup_files.append((backup_local[0], 'Local', common_string.bytes2human(backup_local[1])))
    # cloud backup list
    for backup_cloud in common_cloud.common_cloud_Backup_List():
        backup_files.append((backup_cloud.name, backup_cloud.type,\
            common_string.bytes2human(backup_cloud.size)))
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
    return render_template("admin/admin_server_stats.html", 
                           data_disk=common_system.common_system_Disk_Usage_All(True),
                           data_cpu_usage=common_system.common_system_CPU_Usage(True),
                           data_mem_usage=common_system.common_system_Virtual_Memory(None))


@blueprint.route("/server_stat_slave")
@blueprint.route("/server_stat_slave/")
@login_required
@admin_required
def admin_server_stat_slave():
    return render_template("admin/admin_server_stats_slave.html",
                           data_disk=common_system.common_system_Disk_Usage_All(True),
                           data_cpu_usage=common_system.common_system_CPU_Usage(True),
                           data_mem_usage=common_system.common_system_Virtual_Memory(None))


@blueprint.route("/settings")
@blueprint.route("/settings/")
@login_required
@admin_required
def admin_server_settings():
    return render_template("admin/admin_server_settings.html",
                           form=AdminSettingsForm(request.form))


@blueprint.route("/zfs")
@blueprint.route("/zfs/")
@login_required
@admin_required
def admin_server_zfs():
    return render_template("admin/admin_server_zfs.html",
                           data_zpool=common_zfs.common_zfs_Zpool_List())


@blueprint.route("/link_server")
@blueprint.route("/link_server/")
@login_required
@admin_required
def admin_server_link_server():
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.srv_db_Link_List_Count(),
                                record_name='linked servers',
                                format_total=True,
                                format_number=True,
                                )
    return render_template("admin/admin_link.html",
                           data=g.db.srv_db_Link_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@blueprint.route('/link_delete',methods=["POST"])
@login_required
@admin_required
def admin_link_delete_page():
    g.db.srv_db_Link_Delete(request.form['id'])
    g.db.srv_db_Commit()
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
    line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
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
    line_chart.add('Theater', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Roku',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('Web',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('iOS',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    line_chart.add('Android',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    line_chart.add('Tizen',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    line_chart = line_chart.render(is_unicode=True)
    return render_template("admin/chart/chart_base_usage.html", line_chart=line_chart)


@blueprint.route("/database")
@blueprint.route("/database/")
@login_required
@admin_required
def admin_database_statistics():
    db_stats_count = []
    for row_data in g.db.srv_db_Postgresql_Row_Count():
        db_stats_count.append((row_data[1], locale.format('%d', row_data[2], True)))
    return render_template("admin/admin_server_database_stats.html", 
                           data_db_size=g.db.srv_db_Postgresql_Table_Sizes(),
                           data_db_count=db_stats_count)


@blueprint.route('/browse', defaults={'path': 'home/metaman/'})
@blueprint.route('/browse/', defaults={'path': 'home/metaman/'})
@blueprint.route('/browse/<path:path>')
@login_required
@admin_required
def admin_fs_browse(path):
    browse_file = common_file.common_file_Dir_List('/' + path, None, False, False, True, True)
    browse_parent = []
    build_path = ''
    for path_part in path.split('/'):
        if len(path_part) > 0:
            if build_path == '':
                build_path += path_part # to "skip" leading slash for path
            else:
                build_path += '/' + path_part 
            browse_parent.append((build_path, path_part))
    return render_template("admin/admin_fs_browse.html", file=browse_file,
                           file_parent=browse_parent)


@blueprint.before_request
def before_request():
    g.db = database_base.MK_Server_Database()
    g.db.srv_db_Open(Config.get('DB Connections','PostDBHost').strip(),Config.get('DB Connections','PostDBPort').strip(),Config.get('DB Connections','PostDBName').strip(),Config.get('DB Connections','PostDBUser').strip(),Config.get('DB Connections','PostDBPass').strip())


@blueprint.teardown_request
def teardown_request(exception):
    g.db.srv_db_Close()
