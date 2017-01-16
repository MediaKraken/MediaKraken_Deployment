"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
#from flask_table import Table, Col, create_table
from flask_paginate import Pagination
from fractions import Fraction
blueprint = Blueprint("user", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import pygal
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
from common import common_network_twitch
from common import common_network_vimeo
from common import common_network_youtube
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


# livetv list
@blueprint.route("/livetv/<schedule_date>/<schedule_time>")
@blueprint.route("/livetv/<schedule_date>/<schedule_time>/")
@login_required
def user_livetv_page(schedule_date, schedule_time):
    """
    Display livetv page
    """
    grid_data = '<table style="width:100%" border="2"></tr><th>Station</th><th>Channel</th>'
    for ndx in range(0, 10):
        grid_data += '<th>' + str((int(schedule_time) + (30 * ndx))) + '</th>'
    grid_data += '</tr>'
    channel_data = ""
    md_used = 2
    last_station = None
    for row_data in g.db_connection.db_tv_schedule_by_date(schedule_date):
        if row_data[0] != last_station and last_station is not None:
            grid_data += '<tr><td>' + last_station + '</td><td>' + row_data[1] + '</td>'\
                + channel_data + '</tr>'
            channel_data = ""
            md_used = 2
            last_station = row_data[0]
        else:
            if last_station is None:
                last_station = row_data[0]
        # 1800 seconds per half hour segment
        next_md = row_data[2]['duration'] // 1800
        if next_md == 0:
            next_md = 1
        if md_used + next_md > 12:
            next_md = 12 - md_used
        if md_used == 12:
            pass
        else:
            audio_html = ""
            if 'audioProperties' in row_data[2]:
                for audio_features in row_data[2]['audioProperties']:
                    if audio_features == "cc":
                        audio_html += '<img src="../../../static/images/media_flags/'\
                            'caption-icon.png" alt="Closed Caption"'\
                            ' style="width:15px;height:15px;">'
                    elif audio_features == "stereo":
                        audio_html += '<img src="../../../static/images/media_flags/'\
                            'audio_channels/2.png" alt="Stereo Sound"'\
                            ' style="width:15px;height:15px;">'
                    elif audio_features == "DD 5.1":
                        audio_html += '<img src="../../../static/images/media_flags/'\
                            'audio_channels/6.png" alt="DD 5.1" style="width:15px;height:15px;">'
                    elif audio_features == "SAP":
                        audio_html += '<img src="../../../static/images/media_flags/'\
                            'sap-icon.png" alt="SAP" style="width:15px;height:15px;">'
                    elif audio_features == "dvs":
                        audio_html += '<img src="../../../static/images/media_flags/'\
                            'dvs-icon.png" alt="Descriptive Video Service"'\
                            ' style="width:15px;height:15px;">'
                    elif audio_features == "DD":
                        audio_html += '<img src="../../../static/images/media_flags/'\
                            'audio_codec/dolby_digital.png" alt="Dolby Digital"'\
                            ' style="width:15px;height:15px;">'
# TODO
#    Atmos - Dolby Atmos
#    Dolby
#    dubbed
#    subtitled
#    surround

            video_html = ""
            if 'videoProperties' in row_data[2]:
                for video_features in row_data[2]['videoProperties']:
                    if video_features == "3d":
                        video_html += '<img src="../../../static/images/3D.png" alt="3D"'\
                            ' style="width:15px;height:15px;">'
                    elif video_features == "hdtv":
                        video_html += '<img src="../../../static/images/media_flags/'\
                            'video_resolution.png" alt="HDTV" style="width:15px;height:15px;">'
# TODO
#    enhanced - Enhanced is better video quality than Standard Definition,
                            #but not true High Definition. (720p / 1080i)
#    letterbox
#    sdtv
#    uhdtv - the content is in "UHDTV"; this is provider-dependent and does not imply
                            #any particular resolution or encoding

            rating_html = ""
            if 'ratings' in row_data[2]:
                for rating_features in row_data[2]['ratings']:
                    if rating_features['code'] == "TVG":
                        rating_html += '<img src="../../../static/images/media_flags/'\
                            'content_rating/TV-G.png" alt="TV-G" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVY7":
                        rating_html += '<img src="../../../static/images/media_flags/'\
                            'content_rating/TV-Y7.png" alt="TV-Y7" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVY":
                        rating_html += '<img src="../../../static/images/media_flags/'\
                            'content_rating/TV-Y.png" alt="TV-Y" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVPG":
                        rating_html += '<img src="../../../static/images/media_flags/'\
                            'content_rating/TV-PG.png" alt="TV-PG" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TV14":
                        rating_html += '<img src="../../../static/images/media_flags/'\
                            'content_rating/TV-14.png" alt="TV-14" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVMA":
                        rating_html += '<img src="../../../static/images/media_flags/'\
                            'content_rating/TV-MA.png" alt="TV-MA" style="width:15px;height:15px;">'
            channel_data += '<td colspan="' + str(next_md) + '\">' + row_data[2]['programID']\
                + audio_html + rating_html + '</td>'
            md_used += next_md
    # populate last row
    grid_data += '<tr><td>' + last_station + '</td>' + channel_data + '</tr>'
    return render_template("users/user_livetv_page.html", media=grid_data)


# livetv list detail
@blueprint.route("/livetv_detail/<guid>/")
@blueprint.route("/livetv_detail/<guid>")
@login_required
def user_livetv_detail_page(guid):
    """
    Display live tv detail page
    """
    return render_template("users/user_livetv_page.html")


@blueprint.route('/cast/<action>/<guid>/')
@blueprint.route('/cast/<action>/<guid>')
@login_required
def user_cast(action, guid):
    """
    Display chromecast actions page
    """
    logging.info('cast action: %s', action)
    logging.info('case user: %s', g.current_user)
    if action == 'base':
        pass
    elif action == 'back':
        pass
#    elif action == 'rewind':
#        pass
    elif action == 'stop':
        current_app.com_celery_chrome_stop(json.dumps({'user': g.current_user}))
    elif action == 'play':
        current_app.com_celery_chrome_play(json.dumps({'user': g.current_user, \
            'path': g.db_connection.db_read_media(guid)['mm_media_path']}))
        #cast_proc = subprocess.Popen(['python', './stream2chromecast/stream2chromecast.py', \
        #'-devicename', '10.0.0.56', g.db_connection.db_read_media(guid)['mm_media_path']])
    elif action == 'pause':
        current_app.com_celery_chrome_stop(json.dumps({'user': g.current_user}))
#    elif action == 'ff':
#        pass
    elif action == 'forward':
        pass
    elif action == 'mute':
        current_app.com_celery_chrome_stop(json.dumps({'user': g.current_user}))
    elif action == 'vol_up':
        current_app.com_celery_chrome_stop(json.dumps({'user': g.current_user}))
    elif action == 'vol down':
        current_app.com_celery_chrome_stop(json.dumps({'user': g.current_user}))
    return render_template("users/user_playback_cast.html")


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
    proc_ffserver = subprocess.Popen(['ffmpeg', '-i',\
        g.db_connection.db_media_path_by_uuid(media_guid_index)[0],\
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
        proc = subprocess.Popen(["ffmpeg", "-i", media_path, "-vcodec",\
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


@blueprint.route("/movie_genre")
@blueprint.route("/movie_genre/")
@login_required
def user_movie_genre_page():
    """
    Display movies split up by genre
    """
    media = []
    for row_data in g.db_connection.db_media_movie_count_by_genre(\
            g.db_connection.db_media_uuid_by_class('Movie')):
        media.append((row_data['gen']['name'], locale.format('%d', row_data[1], True),\
            row_data[0]['name'] + ".png"))
    return render_template('users/user_movie_genre_page.html', media=sorted(media))


@blueprint.route("/movie/<genre>")
@blueprint.route("/movie/<genre>/")
@login_required
def user_movie_page(genre):
    """
    Display movie page
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for row_data in g.db_connection.db_web_media_list(\
            g.db_connection.db_media_uuid_by_class('Movie'),\
            list_type='movie', list_genre=genre, list_limit=per_page, group_collection=False,\
            offset=offset, include_remote=True):
        # 0- mm_media_name, 1- mm_media_guid, 2- mm_media_json, 3- mm_metadata_json,
        # 4 - mm_metadata_localimage_json
        logging.info("row2: %s", row_data['mm_media_json'])
        json_image = row_data['mm_metadata_localimage_json']
        # set watched
        try:
            watched_status\
                = row_data['mm_media_json']['UserStats'][current_user.get_id()]['Watched']
        except:
            watched_status = False
        # set synced
        try:
            sync_status = row_data['mm_media_json']['UserStats'][current_user.get_id()]['Synced']
        except:
            sync_status = False
        # set hated
        try:
            poo_status = row_data['mm_media_json']['UserStats'][current_user.get_id()]['Poo']
        except:
            poo_status = False
        # set fav
        try:
            favorite_status\
                = row_data['mm_media_json']['UserStats'][current_user.get_id()]['Favorite']
        except:
            favorite_status = False
        # set mismatch
        try:
            match_status = row_data['MatchFlag']
        except:
            match_status = False
        logging.info("status: %s %s %s %s %s", watched_status, sync_status, poo_status,\
            favorite_status, match_status)
        if 'themoviedb' in json_image['Images'] and 'Poster' in json_image['Images']['themoviedb']\
                and json_image['Images']['themoviedb']['Poster'] is not None:
            media.append((row_data['mm_media_name'], row_data['mm_media_guid'],\
                json_image['Images']['themoviedb']['Poster'],\
                watched_status, sync_status, poo_status, favorite_status, match_status))
        else:
            media.append((row_data['mm_media_name'], row_data['mm_media_guid'], None,\
                watched_status, sync_status, poo_status, favorite_status, match_status))
    total = g.db_connection.db_web_media_list_count(\
        g.db_connection.db_media_uuid_by_class('Movie'), list_type='movie', list_genre=genre,\
        group_collection=False, include_remote=True)
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=total,
                                                  record_name='media',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/user_movie_page.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


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


@blueprint.route("/audio")
@blueprint.route("/audio/")
@login_required
def user_audio_page():
    """
    Obsolete?
    """
    return render_template("users/user_audio_page.html")


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
            media.append((row_data['mm_metadata_album_guid'], row_data['mm_metadata_album_name'],\
                row_data['mm_metadata_album_json']))
        else:
            media.append((row_data['mm_metadata_album_guid'],\
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


@blueprint.route('/server')
@blueprint.route('/server/')
@login_required
def server():
    """
    Display server page
    """
    return render_template("users/user_server.html")


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


@blueprint.route('/class')
@blueprint.route('/class/')
@login_required
def class_display_all():
    """
    Display class list page
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_media_class_list_count(),
                                                  record_name='Media Class',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/user_media_class_list.html',
                           media_class=g.db_connection.db_media_class_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/report_duplicate')
@blueprint.route('/report_duplicate/')
@login_required
def report_display_all_duplicates():
    """
    Display media duplication report page
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_media_duplicate_count(),
                                                  record_name='All Duplicate Media',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/reports/report_all_duplicate_media.html',
                           media=g.db_connection.db_media_duplicate(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/report_duplicate_detail/<guid>/')
@blueprint.route('/report_duplicate_detail/<guid>')
@login_required
def report_display_all_duplicates_detail(guid):
    """
    Display detail of duplicate list
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for media_data in g.db_connection.db_media_duplicate_detail(guid, offset, per_page):
        logging.info("media: %s", media_data['mm_media_ffprobe_json'])
        for stream_data in media_data['mm_media_ffprobe_json']['streams']:
            if stream_data['codec_type'] == 'video':
                media.append((media_data['mm_media_guid'], media_data['mm_media_path'],\
                    str(stream_data['width']) + 'x' + str(stream_data['height']),\
                    media_data['mm_media_ffprobe_json']['format']['duration']))
                break
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.\
                                                      db_media_duplicate_detail_count(guid)[0],
                                                  record_name='copies',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/reports/report_all_duplicate_media_detail.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/report_all')
@blueprint.route('/report_all/')
@login_required
def report_display_all_media():
    """
    Display all media list
    """
    page, per_page, offset = common_pagination.get_page_items()
    media_data = []
    for row_data in g.db_connection.db_known_media(offset, per_page):
        media_data.append((row_data['mm_media_path'],\
            common_string.com_string_bytes2human(os.path.getsize(row_data['mm_media_path']))))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_known_media_count(),
                                                  record_name='All Media',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/reports/report_all_media.html', media=media_data,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/report_known_video')
@blueprint.route('/report_known_video/')
@login_required
def report_display_all_media_known_video():
    """
    Display list of all matched video
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_web_media_list_count(\
                                                      g.db_connection.db_media_uuid_by_class(\
                                                      'Movie')),
                                                  record_name='Known Videos',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/reports/report_all_known_media_video.html',
                           media=g.db_connection.db_web_media_list(\
                               g.db_connection.db_media_uuid_by_class('Movie'),\
                               offset=offset, list_limit=per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/report_top10/<mtype>')
@blueprint.route('/report_top10/<mtype>/')
@login_required
def report_top10(mtype):
    """
    Display top10 pages
    """
    top10_data = None
    if mtype == '1': # all time
        top10_data = g.db_connection.db_usage_top10_alltime()
    elif mtype == '2': # movie
        top10_data = g.db_connection.db_usage_top10_movie()
    elif mtype == '3': # tv show
        top10_data = g.db_connection.db_usage_top10_tv_show()
    elif mtype == '4': # tv episode
        top10_data = g.db_connection.db_usage_top10_tv_episode()
    return render_template('users/reports/report_top10_base.html', media=top10_data)


@blueprint.route('/meta_person_detail/<guid>/')
@blueprint.route('/meta_person_detail/<guid>')
@login_required
def metadata_person_detail(guid):
    """
    Display person detail page
    """
    meta_data = g.db_connection.db_meta_person_by_guid(guid)
    json_metadata = meta_data['mmp_person_meta_json']
    json_imagedata = meta_data['mmp_person_image']
    # person image
    try:
        if json_imagedata['Images']['Poster'] is not None:
            data_person_image = "../../static/meta/images/" + json_imagedata['Images']['Poster']
        else:
            data_person_image = None
    except:
        data_person_image = None
    # also appears in
    meta_also_media = g.db_connection.db_meta_person_as_seen_in(meta_data[0])
    return render_template('users/metadata/meta_people_detail.html',
                           json_metadata=json_metadata,
                           data_person_image=data_person_image,
                           data_also_media=meta_also_media,
                          )


@blueprint.route('/meta_person_list')
@blueprint.route('/meta_person_list/')
@login_required
def metadata_person_list():
    """
    Display person list page
    """
    page, per_page, offset = common_pagination.get_page_items()
    person_list = []
    for person_data in g.db_connection.db_meta_person_list(offset, per_page):
        logging.info('person data: %s', person_data)
        logging.info('im: %s', person_data['mmp_person_image'])
        logging.info('stuff %s', person_data['mmp_meta'])
        if person_data['mmp_person_image'] is not None:
            if 'themoviedb' in person_data['mmp_person_image']['Images']:
                try:
                    person_image = "../../static/meta/images/" + \
                        person_data['mmp_person_image']['Images']['themoviedb']['Profiles'][0] \
                        + person_data['mmp_meta']['profiles'][0]['file_path']
                except:
                    person_image = "../../static/images/person_missing.png"
        else:
            person_image = "../../static/images/person_missing.png"
        person_list.append((person_data['mmp_id'], person_data['mmp_person_name'], person_image))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(\
                                                      'mm_metadata_person'),
                                                  record_name='People',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_people_list.html',
                           media_person=person_list,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_music_list')
@blueprint.route('/meta_music_list/')
@login_required
def metadata_music_list():
    """
    Display metdata music list
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(\
                                                      'mm_metadata_music'),
                                                  record_name='music',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_music_list.html',
                           media_person=g.db_connection.db_meta_music_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_music_album_list')
@blueprint.route('/meta_music_album_list/')
@login_required
def metadata_music_album_list():
    """
    Display metadata of album list
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(\
                                                      'mm_metadata_music_album'),
                                                  record_name='music album',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_music_album_list.html',
                           media_person=g.db_connection.db_meta_music_album_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_movie_collection_list')
@blueprint.route('/meta_movie_collection_list/')
@login_required
def metadata_movie_collection_list():
    """
    Display movie collection metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for row_data in g.db_connection.db_collection_list(offset, per_page):
        try:
            media.append((row_data['mm_metadata_collection_guid'],\
                row_data['mm_metadata_collection_name'],\
                row_data['mm_metadata_collection_imagelocal_json']['Poster']))
        except:
            media.append((row_data['mm_metadata_collection_guid'],\
                row_data['mm_metadata_collection_name'], None))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(\
                                                      'mm_metadata_collection'),
                                                  record_name='movie collection(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_movie_collection_list.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_movie_collection_detail/<guid>/')
@blueprint.route('/meta_movie_collection_detail/<guid>')
@login_required
def metadata_movie_collection_detail(guid):
    """
    Display movie collection metadata detail
    """
    data_metadata = g.db_connection.db_collection_read_by_guid(guid)
    json_metadata = data_metadata['mm_metadata_collection_json']
    json_imagedata = data_metadata['mm_metadata_collection_imagelocal_json']
    # poster image
    try:
        if json_imagedata['Poster'] is not None:
            data_poster_image = json_imagedata['Poster']
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_imagedata['Backdrop'] is not None:
            data_background_image = json_imagedata['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template('users/metadata/meta_movie_collection_detail.html',
                           data_name=json_metadata['name'],
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image,
                           json_metadata=json_metadata
                          )


@blueprint.route('/media_status/<guid>/<media_type>/<event_type>/', methods=['GET', 'POST'])
@blueprint.route('/media_status/<guid>/<media_type>/<event_type>', methods=['GET', 'POST'])
@login_required
def media_status(guid, media_type, event_type):
    """
    Set media status for specified media, user
    """
    logging.info('media status: %s %s %s', guid, media_type, event_type)
    if media_type == "movie":
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
        return redirect(url_for('user.user_movie_page', guid=guid))
    elif media_type == "tv":
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
        return redirect(url_for('user.user_tv_page', guid=guid))
    else:
        logging.error("Invalid media type: %s", media_type)


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
