"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from MediaKraken.extensions import (
    fpika,
)
from flask import Blueprint, render_template, g
from flask_login import login_required, current_user

blueprint = Blueprint("user_playback", __name__,
                      url_prefix='/users', static_folder="../static")
import uuid
import json
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/playalbum/<guid>')
@login_required
def user_album_player(guid):
    """
    Obsolete?
    """
    return render_template("users/user_album_playback.html",
                           data_desc=g.db_connection.db_meta_album_by_guid(
                               guid),
                           data_song_list=g.db_connection.db_meta_songs_by_album_guid(guid))


@blueprint.route('/playvideo_videojs/<mtype>/<guid>/<chapter>/<audio>/<sub>', methods=['GET',
                                                                                       'POST'])
@login_required
def user_video_player_videojs(mtype, guid, chapter, audio, sub):
    """
    Display video playback page
    """
    # TODO will need start time/etc for resume function
    common_global.es_inst.com_elastic_index('info',
                                            {"videojs": mtype, 'guid': guid, 'chapter': chapter,
                                             'audio': audio, 'sub': sub})
    # grab the guid from the comboindex
    media_path = g.db_connection.db_media_path_by_uuid(guid)
    # set ffpmeg options with the play_data
    atracks = '-map ' + audio
    if sub is not None:
        subtracks = 'subtitles=\"' + media_path + '\" language=' + sub
    else:
        subtracks = ''
    # fire up ffmpeg process
    if mtype == "hls":
        # must be done here so can send commands for the right stream
        target_uuid = str(uuid.uuid4())
        vid_name = "./static/cache/" + target_uuid + ".m3u8"

        # ffmpeg -i input.mp4 -profile:v baseline -level 3.0 -s 640x360
        # -start_number 0 -hls_time 10 -hls_list_size 0 -f hls index.m3u8

        ch = fpika.channel()
        ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
                         body=json.dumps({'Type': 'Play', 'Subtype': 'HLS',
                                          'Input File': media_path,
                                          'Audio Track': atracks,
                                          'Subtitle Track': subtracks,
                                          'Target UUID': target_uuid,
                                          'User': current_user.get_id()}))
        fpika.return_channel(ch)

        # TODO how to know what to return here.....slave could be anywhere on swarm
        pass_guid = 'https://th-mediakraken-1' + '/' + vid_name
        # pass_guid = '//s3.amazonaws.com/_bc_dml/example-content/tears-of-steel/playlist.m3u8'
    else:
        pass_guid = guid
    common_global.es_inst.com_elastic_index('info', {"hls path": pass_guid})
    return render_template("users/user_playback_videojs.html", data_desc=('Movie title'),
                           data_guid=pass_guid,
                           data_mtype=mtype)


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
