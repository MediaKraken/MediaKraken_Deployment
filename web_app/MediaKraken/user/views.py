"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
from fractions import Fraction
blueprint = Blueprint("user", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import datetime
import uuid
import json
import subprocess
import os
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_google
from common import common_pagination
from common import common_string
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()


def flash_errors(form):
    """
    Display each error on top of form
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@blueprint.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload_image():
    """
    Allow user to upload image
    """
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo saved.")
        return redirect(url_for('show', id=rec.id))
    return render_template('upload.html')


@blueprint.route("/")
@login_required
def members():
    """
    Display main members page
    """
    resume_list = []
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_read_media_new_count(7),
                                                  record_name='new and hot',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template("users/members.html", data_resume_media=resume_list,
                           data_new_media=g.db_connection.db_read_media_new(7, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


# home media
@blueprint.route('/home_media')
@blueprint.route('/home_media/')
@login_required
def user_home_media_list():
    """
    Display mage page for home media
    """
    return render_template("users/user_home_media_list.html")


@blueprint.route('/playvideo/<guid>/')
@blueprint.route('/playvideo/<guid>')
@login_required
def user_video_player(guid):
    """
    Obsolete?
    """
    # grab the guid from the comboindex
    media_guid_index = request.form["Video_Track"]
    # call ffpmeg with the play_data
    audio_track_index = request.form["Video_Play_Audio_Track"]
    subtitle_track_index = request.form["Video_Play_Subtitles"]
    # launch ffmpeg to ffserver procecss
    proc_ffserver = subprocess.Popen(['ffmpeg', '-i',
        g.db_connection.db_media_path_by_uuid(media_guid_index)[0],
        'http://localhost:8900/stream.ffm'], shell=False)
    logging.info("FFServer PID: %s", proc_ffserver.pid)
    return render_template("users/user_playback.html", data_desc=('Movie title'))


@blueprint.route('/playvideo_videojs/<mtype>/<guid>/')
@blueprint.route('/playvideo_videojs/<mtype>/<guid>')
@login_required
def user_video_player_videojs(mtype, guid):
    """
    Display video playback page
    """
    logging.info("videojs: %s %s", mtype, guid)
    # grab the guid from the comboindex
    # use try since people can go here "by-hand"
    try:
        media_guid_index = request.form["Video_Track"]
    except:
        abort(404)
    media_path = g.db_connection.db_media_path_by_uuid(media_guid_index)[0]
    if media_path is None:
        abort(404)
    # set ffpmeg options with the play_data
    audio_track_index = request.form["Video_Play_Audio_Track"]
    logging.info("aud: %s", audio_track_index)
    atracks=['-map ' + audio_track_index] # 0:0 as example # pylint: disable=C0326
    subtitle_track_index = request.form["Video_Play_Subtitles"]
    logging.info("sub: %s", subtitle_track_index)
    if subtitle_track_index is not None:
        subtracks = ['subtitles=' + media_path, 'language=' + subtitle_track_index]
    else:
        # TODO example from file
        subtracks = ['subtitles=subtitle.srt']
    # fire up ffmpeg process
    if mtype == "hls":
        vid_name = "./static/cache/" + str(uuid.uuid4()) + ".m3u8"
        acodecs = ['aac', '-ac:a:0', '2', '-vbr', '5'] # pylint: disable=C0326
        proc = subprocess.Popen(["ffmpeg", "-i", media_path, "-vcodec",
            "libx264", "-preset", "veryfast", "-acodec"] + acodecs + atracks\
            + ["-vf"] + subtracks\
            + ["yadif=0:0:0", vid_name], shell=False)
        logging.info("FFMPEG Pid: %s", proc.pid)

#ffmpeg -i input.mp4 -profile:v baseline -level 3.0 -s 640x360
# -start_number 0 -hls_time 10 -hls_list_size 0 -f hls index.m3u8

        pass_guid = 'http://10.0.0.179' + '/user/static/cache/' + vid_name
        #pass_guid = '//s3.amazonaws.com/_bc_dml/example-content/tears-of-steel/playlist.m3u8'
    else:
        pass_guid = guid
    logging.info("hls path: %s", pass_guid)
    return render_template("users/user_playback_videojs.html", data_desc=('Movie title'),
                           data_guid=pass_guid,
                           data_mtype=mtype)


@blueprint.route('/playalbum/<guid>/')
@blueprint.route('/playalbum/<guid>')
@login_required
def user_album_player(guid):
    """
    Obsolete?
    """
    return render_template("users/user_album_playback.html",
                           data_desc=g.db_connection.db_meta_album_by_guid(guid),
                           data_song_list=g.db_connection.db_meta_songs_by_album_guid(guid))


#@blueprint.route("/video")
#@blueprint.route("/video/")
#@login_required
#def user_video_page():
#    page, per_page, offset = common_pagination.get_page_items()
#    media = []
#    # class_guid, list_type, list_genre = None, list_limit = 500000, group_collection = False, offset = 0
#    media.append((g.db_connection.db_web_media_list(xxxx, 'in_progress', None, per_page, False, offset))) # extra parans so adds list
#    total = g.db_connection.db_web_media_list_count(xxxx, 'in_progress', None, False)
#    media.append((g.db_connection.db_web_media_list(xxxx, 'recent_addition', None, per_page, False, offset)))
#    total += g.db_connection.db_web_media_list_count(xxxx, 'recent_addition', None, False)
#    media.append((g.db_connection.db_web_media_list(xxxx, 'video', None, per_page, False, offset)))
#    total += g.db_connection.db_web_media_list_count(xxxx, 'video', None, False)
#    pagination = common_pagination.get_pagination(page=page,
#                                per_page=per_page,
#                                total=total,
#                                record_name='Media',
#                                format_total=True,
#                                format_number=True,
#                                )
#    return render_template('users/user_video_page.html', media=media,
#                           page=page,
#                           per_page=per_page,
#                           pagination=pagination,
#                           )


@blueprint.route("/album_list")
@blueprint.route("/album_list/")
@login_required
def user_album_list_page():
    """
    Display album page
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for row_data in g.db_connection.db_media_album_list(offset, per_page):
        if 'mm_metadata_album_json' in row_data:
            media.append((row_data['mm_metadata_album_guid'], row_data['mm_metadata_album_name'],
                row_data['mm_metadata_album_json']))
        else:
            media.append((row_data['mm_metadata_album_guid'],
                row_data['mm_metadata_album_name'], None))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_media_album_count(),
                                                  record_name='music albums',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template("users/user_music_album_page.html", media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/media')
@blueprint.route('/media/')
@login_required
def user_media_list():
    """
    Display main media page
    """
    return render_template("users/user_media_list.html")


@blueprint.route('/search/<name>/')
@blueprint.route('/search/<name>')
@login_required
def search(name):
    """
    Search media
    """
    sql = 'select count(*) from users where name like ?'
    args = ('%{}%'.format(name), )
    g.cur.execute(sql, args)
    try:
        total = g.cur.fetchone()[0]
    except:
        total = 0
    page, per_page, offset = common_pagination.get_page_items()
    sql = 'select * from users where name like %s limit {}, {}'
    g.cur.execute(sql.format(offset, per_page), args)
    users = g.cur.fetchall()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=total,
                                                  record_name='Users',
                                                 )
    return render_template('users/user_report_all_known_media_video.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


# https://github.com/Bouni/HTML5-jQuery-Flask-file-upload
@blueprint.route('/upload', methods=['POST'])
@blueprint.route('/upload/', methods=['POST'])
@login_required
def upload():
    """
    Handle file upload from user
    """
    if request.method == 'POST':
        file_handle = request.files['file']
        if file_handle and allowed_file(file_handle.filename):
            now = datetime.now()
            filename = os.path.join(app.config_handle['UPLOAD_FOLDER'], "%s.%s"\
                % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file_handle.filename.rsplit('.', 1)[1]))
            file_handle.save(filename)
            return jsonify({"success": True})


@blueprint.route('/movie_status/<guid>/<event_type>/', methods=['GET', 'POST'])
@blueprint.route('/movie_status/<guid>/<event_type>', methods=['GET', 'POST'])
@login_required
def movie_status(guid, event_type):
    """
    Set media status for specified media, user
    """
    logging.info('movie status: %s %s', guid, event_type)
    if event_type == "watched":
        g.db_connection.db_media_watched_status_update(guid, current_user.get_id(), True)
        return json.dumps({'status':'OK'})
    elif event_type == "sync":
        return redirect(url_for('user.sync_edit', guid=guid))
    elif event_type == "favorite":
        g.db_connection.db_media_favorite_status_update(guid, current_user.get_id(), True)
        return json.dumps({'status':'OK'})
    elif event_type == "poo":
        g.db_connection.db_media_poo_status_update(guid, current_user.get_id(), True)
        return json.dumps({'status':'OK'})
    elif event_type == "mismatch":
        pass
    return redirect(url_for('user_movie_genre.user_movie_page', genre='All'))


@blueprint.route('/tv_status/<guid>/<event_type>/', methods=['GET', 'POST'])
@blueprint.route('/tv_status/<guid>/<event_type>', methods=['GET', 'POST'])
@login_required
def tv_status(guid, event_type):
    """
    Set media status for specified media, user
    """
    logging.info('tv status: %s %s', guid, event_type)
    if event_type == "watched":
        pass
    elif event_type == "sync":
        pass
    elif event_type == "favorite":
        pass
    elif event_type == "poo":
        pass
    elif event_type == "mismatch":
        pass
    return redirect(url_for('user_tv.user_tv_page'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception): # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
