"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from quart import Blueprint, render_template, g, request, \
    redirect, url_for, abort, flash, session
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")
import uuid
import json
import subprocess
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_pagination
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


@blueprint.route("/")
@login_required
async def members():
    """
    Display main members page
    """
    resume_list = []
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_read_media_new_count(
                                                      7),
                                                  record_name='new and hot',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return await render_template("users/members.html", data_resume_media=resume_list,
                           data_new_media=g.db_connection.db_read_media_new(
                               7, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


# home media
@blueprint.route('/home_media', methods=['GET', 'POST'])
@blueprint.route('/home_media/', methods=['GET', 'POST'])
@login_required
async def user_home_media_list():
    """
    Display mage page for home media
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    if session['search_text'] is not None:
        # TODO wrong movie query
        metadata = g.db_connection.db_meta_movie_list(offset, per_page, search_text)
    else:
        metadata = g.db_connection.db_meta_movie_list(offset, per_page)
    return await render_template("users/user_home_media_list.html", media=media)


@blueprint.route('/playvideo/<guid>/')
@blueprint.route('/playvideo/<guid>')
@login_required
async def user_video_player(guid):
    """
    Obsolete?
    """
    # grab the guid from the comboindex
    media_guid_index = await request.form["Video_Track"]
    # call ffpmeg with the play_data
    audio_track_index = await request.form["Video_Play_Audio_Track"]
    subtitle_track_index = await request.form["Video_Play_Subtitles"]
    # launch ffmpeg to ffserver procecss
    proc_ffserver = subprocess.Popen(['ffmpeg', '-i',
                                      g.db_connection.db_media_path_by_uuid(
                                          media_guid_index)[0],
                                      'http://localhost/stream.ffm'], shell=False)
    common_global.es_inst.com_elastic_index('info', {"FFServer PID": proc_ffserver.pid})
    return await render_template("users/user_playback.html", data_desc=('Movie title'))


@blueprint.route('/playvideo_videojs/<mtype>/<guid>/')
@blueprint.route('/playvideo_videojs/<mtype>/<guid>')
@login_required
async def user_video_player_videojs(mtype, guid):
    """
    Display video playback page
    """
    common_global.es_inst.com_elastic_index('info', {"videojs": mtype, 'guid': guid})
    # grab the guid from the comboindex
    # use try since people can go here "by-hand"
    try:
        media_guid_index = await request.form["Video_Track"]
    except:
        abort(404)
    media_path = g.db_connection.db_media_path_by_uuid(media_guid_index)[0]
    if media_path is None:
        abort(404)
    # set ffpmeg options with the play_data
    audio_track_index = await request.form["Video_Play_Audio_Track"]
    common_global.es_inst.com_elastic_index('info', {"aud": audio_track_index})
    # 0:0 as example # pylint: disable=C0326
    atracks = ['-map ' + audio_track_index]
    subtitle_track_index = await request.form["Video_Play_Subtitles"]
    common_global.es_inst.com_elastic_index('info', {"sub": subtitle_track_index})
    if subtitle_track_index is not None:
        subtracks = ['subtitles=' + media_path,
                     'language=' + subtitle_track_index]
    else:
        # TODO example from file
        subtracks = ['subtitles=subtitle.srt']
    # fire up ffmpeg process
    if mtype == "hls":
        vid_name = "./static/cache/" + str(uuid.uuid4()) + ".m3u8"
        acodecs = ['aac', '-ac:a:0', '2', '-vbr', '5']  # pylint: disable=C0326
        proc = subprocess.Popen(["ffmpeg", "-i", media_path, "-vcodec",
                                 "libx264", "-preset", "veryfast", "-acodec"] + acodecs + atracks
                                + ["-vf"] + subtracks
                                + ["yadif=0:0:0", vid_name], shell=False)
        common_global.es_inst.com_elastic_index('info', {"FFMPEG Pid": proc.pid})

        # ffmpeg -i input.mp4 -profile:v baseline -level 3.0 -s 640x360
        # -start_number 0 -hls_time 10 -hls_list_size 0 -f hls index.m3u8

        pass_guid = 'http://10.0.0.179' + '/user/static/cache/' + vid_name
        # pass_guid = '//s3.amazonaws.com/_bc_dml/example-content/tears-of-steel/playlist.m3u8'
    else:
        pass_guid = guid
    common_global.es_inst.com_elastic_index('info', {"hls path": pass_guid})
    return await render_template("users/user_playback_videojs.html", data_desc=('Movie title'),
                           data_guid=pass_guid,
                           data_mtype=mtype)


@blueprint.route('/playalbum/<guid>/')
@blueprint.route('/playalbum/<guid>')
@login_required
async def user_album_player(guid):
    """
    Obsolete?
    """
    return await render_template("users/user_album_playback.html",
                           data_desc=g.db_connection.db_meta_album_by_guid(
                               guid),
                           data_song_list=g.db_connection.db_meta_songs_by_album_guid(guid))


@blueprint.route('/movie_status/<guid>/<event_type>/', methods=['GET', 'POST'])
@blueprint.route('/movie_status/<guid>/<event_type>', methods=['GET', 'POST'])
@login_required
async def movie_status(guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'movie status': guid, 'event': event_type})
    if event_type == "sync":
        return redirect(url_for('user.sync_edit', guid=guid))
    else:
        g.db_connection.db_media_rating_update(
            guid, current_user.get_id(), event_type)
        return json.dumps({'status': 'OK'})


@blueprint.route('/movie_metadata_status/<guid>/<event_type>/', methods=['GET', 'POST'])
@blueprint.route('/movie_metadata_status/<guid>/<event_type>', methods=['GET', 'POST'])
@login_required
async def movie_metadata_status(guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'movie metadata status': guid,
                                                     'event': event_type})
    g.db_connection.db_meta_movie_status_update(
        guid, current_user.get_id(), event_type)
    return json.dumps({'status': 'OK'})


@blueprint.route('/tv_status/<guid>/<event_type>/', methods=['GET', 'POST'])
@blueprint.route('/tv_status/<guid>/<event_type>', methods=['GET', 'POST'])
@login_required
async def tv_status(guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'tv status': guid, 'event': event_type})
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


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception):  # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
