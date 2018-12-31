# -*- coding: utf-8 -*-

import json
import os
import pygal
import sys
import uuid

sys.path.append('..')
from flask import Blueprint, render_template, g, request, flash, \
    url_for, redirect, abort
from flask_login import login_required

blueprint = Blueprint("admins", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from werkzeug.utils import secure_filename
from functools import wraps
from functools import partial
from MediaKraken.admins.forms import AdminSettingsForm
from MediaKraken.admins.forms import BookAddForm

from common import common_config_ini
from common import common_internationalization
from common import common_global
from common import common_hash
from common import common_network
from common import common_string
from common import common_system
from common import common_version
from common import common_zfs
import database as database_base

ALLOWED_EXTENSIONS = set(['py', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

outside_ip = None
option_config_json, db_connection = common_config_ini.com_config_read()


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
        common_global.es_inst.com_elastic_index('info', {"admin access attempt by":
                                                             current_user.get_id()})
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
    for key, value in common_network.mk_network_ip_addr().items():
        nic_data.append(key + ' ' + value[0][1])
    data_alerts_dismissable = []
    data_alerts = []
    # read in the notifications
    for row_data in g.db_connection.db_notification_read():
        if row_data['mm_notification_dismissable']:  # check for dismissable
            data_alerts_dismissable.append((row_data['mm_notification_guid'],
                                            row_data['mm_notification_text'],
                                            row_data['mm_notification_time']))
        else:
            data_alerts.append((row_data['mm_notification_guid'],
                                row_data['mm_notification_text'], row_data['mm_notification_time']))
    data_transmission_active = False
    if g.db_connection.db_opt_status_read()['mm_options_json']['Transmission']['Host'] is not None:
        data_transmission_active = True
    # set the scan info
    data_scan_info = []
    scanning_json = g.db_connection.db_opt_status_read()['mm_status_json']
    if 'Status' in scanning_json:
        data_scan_info.append(('System', scanning_json['Status'], scanning_json['Pct']))
    for dir_path in g.db_connection.db_audit_path_status():
        data_scan_info.append((dir_path[0], dir_path[1]['Status'], dir_path[1]['Pct']))
    if os.environ['SWARMIP'] != 'None':
        mediakraken_ip = os.environ['SWARMIP']
    else:
        mediakraken_ip = os.environ['HOST_IP']
    return render_template("admin/admins.html",
                           data_user_count=common_internationalization.com_inter_number_format(
                               g.db_connection.db_user_list_name_count()),
                           data_server_info_server_name=data_server_info_server_name,
                           data_host_ip=mediakraken_ip,
                           data_server_info_server_ip=nic_data,
                           data_server_info_server_ip_external=outside_ip,
                           data_server_info_server_version=common_version.APP_VERSION,
                           data_server_uptime=common_system.com_system_uptime(),
                           data_active_streams=common_internationalization.com_inter_number_format(
                               0),
                           data_alerts_dismissable=data_alerts_dismissable,
                           data_alerts=data_alerts,
                           data_count_media_files=common_internationalization.com_inter_number_format(
                               g.db_connection.db_known_media_count()),
                           data_count_matched_media=common_internationalization.com_inter_number_format(
                               g.db_connection.db_matched_media_count()),
                           data_count_streamed_media=common_internationalization.com_inter_number_format(
                               0),
                           data_library=common_internationalization.com_inter_number_format(
                               g.db_connection.db_table_count('mm_media_dir')),
                           data_share=common_internationalization.com_inter_number_format(
                               g.db_connection.db_table_count('mm_media_share')),
                           data_transmission_active=data_transmission_active,
                           data_scan_info=data_scan_info,
                           data_messages=data_messages,
                           data_count_meta_fetch=common_internationalization.com_inter_number_format(
                               g.db_connection.db_table_count('mm_download_que')),
                           )


@blueprint.route("/admin_sidenav")
@login_required
@admin_required
def admin_sidenav():
    return render_template("admin/admin_sidenav.html")


@blueprint.route("/messages", methods=["GET", "POST"])
@login_required
@admin_required
def admin_messages():
    """
    List all NAS devices
    """
    messages = []
    return render_template("admin/admin_messages.html", data_messages=messages)


@blueprint.route("/nas", methods=["GET", "POST"])
@login_required
@admin_required
def admin_nas():
    """
    List all NAS devices
    """
    nas_devices = []
    return render_template("admin/admin_nas.html", data_nas=nas_devices)


@blueprint.route('/books_add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_books_add():
    """
    Display books add page
    """
    if request.method == 'POST':
        class_uuid = g.db_connection.db_media_uuid_by_class('Book')
        for book_item in request.form['book_list'].split('\r'):
            if len(book_item) > 2:
                media_id = str(uuid.uuid4())
                g.db_connection.db_insert_media(media_id, None, class_uuid,
                                                None, None, None)
                g.db_connection.db_download_insert('Z', 0, json.dumps({'MediaID': media_id,
                                                                       'Path': None,
                                                                       'ClassID': class_uuid,
                                                                       'Status': None,
                                                                       'MetaNewID': str(
                                                                           uuid.uuid4()),
                                                                       'ProviderMetaID': book_item.strip()}))
        g.db_connection.db_commit()
        return redirect(url_for('admins.admin_books_add'))
    form = BookAddForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        pass
    return render_template("admin/admin_books_add.html", form=form)


@blueprint.route("/settings", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_server_settings():
    """
    Display server settings page
    """
    settings_json = g.db_connection.db_opt_status_read()[0]
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
        settings_json['API']['musicbrainz'] = data.com_hash_gen_crypt_encode(
            request.form['docker_musicbrainz_code'])
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
        g.db_connection.db_opt_update(settings_json)
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
    return render_template("admin/admin_server_settings.html",
                           form=AdminSettingsForm(request.form),
                           settings_json=settings_json,
                           mediabrainz_api_key=mediabrainz_api_key,
                           opensubtitles_api_key=opensubtitles_api_key
                           )


@blueprint.route("/zfs")
@login_required
@admin_required
def admin_server_zfs():
    """
    Display zfs admin page
    """
    return render_template("admin/admin_server_zfs.html",
                           data_zpool=common_zfs.com_zfs_zpool_list())


@blueprint.route("/cloud")
@login_required
@admin_required
def admin_cloud_dropbox():
    """
    browse cloud via libcloud
    """
    return render_template("admin/admin_cloud.html")


@blueprint.route("/chart_browser")
@login_required
@admin_required
def admin_chart_browser():
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6,
                               25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None,
                              None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66,
                          58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9,
                              9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart = line_chart.render(is_unicode=True)
    return render_template("admin/chart/chart_base_usage.html", line_chart=line_chart)


@blueprint.route("/chart_client_usage")
@login_required
@admin_required
def admin_chart_client_usage():
    line_chart = pygal.Line()
    line_chart.title = 'Client usage'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Theater', [None, None, 0, 16.6,
                               25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Roku', [None, None, None, None,
                            None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('Web', [85.8, 84.6, 84.7, 74.5, 66,
                           58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('iOS', [14.2, 15.4, 15.3, 8.9, 9,
                           10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.add('Android', [14.2, 15.4, 15.3, 8.9,
                               9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.add('Tizen', [14.2, 15.4, 15.3, 8.9,
                             9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart = line_chart.render(is_unicode=True)
    return render_template("admin/chart/chart_base_usage.html", line_chart=line_chart)


@blueprint.route("/database")
@login_required
@admin_required
def admin_database_statistics():
    """
    Display database statistics page
    """
    db_stats_count = []
    db_stats_total = 0
    for row_data in g.db_connection.db_pgsql_row_count():
        db_stats_total += row_data[2]
        db_stats_count.append((row_data[1],
                               common_internationalization.com_inter_number_format(row_data[2])))
    db_stats_count.append(
        ('Total records:', common_internationalization.com_inter_number_format(db_stats_total)))
    db_size_data = []
    db_size_total = 0
    for row_data in g.db_connection.db_pgsql_table_sizes():
        db_size_total += row_data['total_size']
        db_size_data.append(
            (row_data['relation'], common_string.com_string_bytes2human(row_data['total_size'])))
    db_size_data.append(('Total Size:', common_string.com_string_bytes2human(db_stats_total)))
    return render_template("admin/admin_server_database_stats.html",
                           data_db_size=db_size_data,
                           data_db_count=db_stats_count,
                           data_workers=db_connection.db_parallel_workers())


@blueprint.route('/', defaults={'path': ''}, endpoint='listdir')
@blueprint.route('/<path:path>/list', endpoint='listdirpath')
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
        files = list(
            map(partial(gather_fileinfo, path, ospath), os.listdir(ospath)))
        files = list(filter(lambda file: file is not None, files))
        files.sort(key=lambda i: (
                                         i['type'] == 'file' and '1' or '0') + i[
                                     'filename'].lower())
        return render_template('admin/admin_fs_browse.html',
                               files=files,
                               parent=os.path.dirname(path),
                               path=path)
    except IOError:
        abort(404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_handle = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file_handle.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_handle and allowed_file(file_handle.filename):
            filename = secure_filename(file_handle.filename)
            file_handle.save(os.path.join('/mediakraken/uploads', filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


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
