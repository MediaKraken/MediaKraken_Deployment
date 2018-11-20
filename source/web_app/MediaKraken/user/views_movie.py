"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from fractions import Fraction
from shlex import split

from flask import Blueprint, render_template, g, request, \
    redirect, url_for
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user_movie", __name__,
                      url_prefix='/users', static_folder="../static")
import subprocess
import natsort
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_string
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/movie_detail/<guid>', methods=['GET', 'POST'])
@login_required
def movie_detail(guid):
    """
    Display move detail page
    """
    if request.method == 'POST':
        # do NOT need to check for play video here,
        # it's routed by the event itself in the html via the 'action' clause
        if request.form['status'] == 'Watched':
            g.db_connection.db_meta_movie_status_update(
                guid, current_user.get_id(), False)
            return redirect(url_for('user_movie.movie_detail', guid=guid))
        elif request.form['status'] == 'Unwatched':
            g.db_connection.db_meta_movie_status_update(
                guid, current_user.get_id(), True)
            return redirect(url_for('user_movie.movie_detail', guid=guid))
        elif request.form['status'] == 'Sync':
            return redirect(url_for('user_sync.sync_edit', guid=guid))
        elif request.form['status'] == 'Cast':
            # TODO submit cast comment via rabbitmq
            # grab the guid from the comboindex
            media_guid_index = request.form["Video_Track"]
            # call ffpmeg with the play_data
            audio_track_index = request.form["Video_Play_Audio_Track"]
            subtitle_track_index = request.form["Video_Play_Subtitles"]
            # launch ffmpeg to ffserver procecss
            proc_ffserver = subprocess.Popen(split('ffmpeg  -i \"',
                                                   g.db_connection.db_media_path_by_uuid(
                                                       media_guid_index)[
                                                       0] + '\" http://localhost/stream.ffm'))
            common_global.es_inst.com_elastic_index('info', {"FFServer PID": proc_ffserver.pid})
            return redirect(url_for('user_movie.movie_detail', guid=guid))
        elif request.form['status'] == 'WebPlay':
            return redirect(url_for('user_playback.user_video_player_videojs', mtype='hls',
                                    guid=request.form['Video_Track'], chapter=1,
                                    audio=request.form['Video_Play_Audio_Track'],
                                    sub=request.form['Video_Play_Subtitles']))
    else:
        metadata_data = g.db_connection.db_meta_movie_by_media_uuid(guid)
        # fields returned
        # metadata_data['mm_metadata_json']
        # metadata_data['mm_metadata_localimage_json']

        # not sure if the following with display anymore
        # # vote count format
        # data_vote_count = common_internationalization.com_inter_number_format(
        #     metadata_data['mm_metadata_json']['Meta']['themoviedb']['Meta']['vote_count'])
        # # build gen list
        # genres_list = ''
        # for ndx in range(0, len(
        #         metadata_data['mm_metadata_json']['Meta']['themoviedb']['Meta']['genres'])):
        #     genres_list += (
        #                 metadata_data['mm_metadata_json']['Meta']['themoviedb']['Meta']['genres'][
        #                     ndx]['name']
        #                 + ', ')
        # # build production list
        # production_list = ''
        # for ndx in range(0,
        #                  len(metadata_data['mm_metadata_json']['Meta']['themoviedb']['Meta']['production_companies'])):
        #     production_list \
        #         += (metadata_data['mm_metadata_json']['Meta']['themoviedb']['Meta']['production_companies'][ndx]['name']
        #             + ', ')
        # # budget format
        # budget = common_internationalization.com_inter_number_format(
        #     metadata_data['mm_metadata_json']['Meta']['themoviedb']['Meta']['budget'])
        # # revenue format
        # revenue = common_internationalization.com_inter_number_format(
        #     metadata_data['mm_metadata_json']['Meta']['themoviedb']['Meta']['revenue'])


        # not all files have ffmpeg that didn't fail
        if json_ffmpeg is None:
            aspect_ratio = "NA"
            bitrate = "NA"
            file_size = "NA"
            hours = 0
            minutes = 0
            seconds = 0
            data_resolution = "NA"
            data_codec = "NA"
            data_file = "NA"
        else:
            # aspect ratio
            try:
                aspect_ratio = str(Fraction(json_ffmpeg['streams'][0]['width'],
                                            json_ffmpeg['streams'][0]['height'])).replace('/', ':')
            except:
                aspect_ratio = 'NA'
            # bitrate
            try:
                bitrate = common_string.com_string_bytes2human(
                    float(json_ffmpeg['format']['bit_rate']))
            except:
                bitrate = 'NA'
            # file size
            file_size = common_string.com_string_bytes2human(
                float(json_ffmpeg['format']['size']))
            # calculate a better runtime
            try:
                minutes, seconds = divmod(
                    float(json_ffmpeg['format']['duration']), 60)
                hours, minutes = divmod(minutes, 60)
            except:
                hours = 0
                minutes = 0
                seconds = 0
            try:
                data_resolution = str(json_ffmpeg['streams'][0]['width']) + 'x' \
                                  + str(json_ffmpeg['streams'][0]['height'])
            except:
                data_resolution = 'NA'
            data_codec = json_ffmpeg['streams'][0]['codec_name']
            data_file = json_ffmpeg['format']['filename']
        # check to see if there are other version of this video file (dvd, hddvd, etc)
        vid_versions = g.db_connection.db_media_by_metadata_guid(data[1],
                                                                 g.db_connection.db_media_uuid_by_class(
                                                                     'Movie'))
        common_global.es_inst.com_elastic_index('info', {"vid_versions": vid_versions})
        # audio and sub streams
        audio_streams = []
        subtitle_streams = [(None, 'None')]
        if json_ffmpeg is not None:
            for stream_info in json_ffmpeg['streams']:
                stream_language = ''
                stream_title = ''
                stream_codec = ''
                try:
                    stream_language = stream_info['tags']['language'] + ' - '
                except:
                    pass
                try:
                    stream_title = stream_info['tags']['title'] + ' - '
                except:
                    pass
                try:
                    stream_codec \
                        = stream_info['codec_long_name'].rsplit('(', 1)[1].replace(')', '') \
                          + ' - '
                except:
                    pass
                if stream_info['codec_type'] == 'audio':
                    audio_streams.append((len(audio_streams), (stream_codec + stream_language
                                                               + stream_title)[:-3]))
                elif stream_info['codec_type'] == 'subtitle':
                    subtitle_streams.append(
                        (len(subtitle_streams), stream_language[:-2]))
        # poster image
        try:
            if json_imagedata['Images']['themoviedb']['Poster'] is not None:
                data_poster_image = json_imagedata['Images']['themoviedb']['Poster']
            else:
                data_poster_image = None
        except:
            data_poster_image = None
        # background image
        try:
            if json_imagedata['Images']['themoviedb']['Backdrop'] is not None:
                data_background_image = json_imagedata['Images']['themoviedb']['Backdrop']
            else:
                data_background_image = None
        except:
            data_background_image = None
        # grab reviews
        review = []
        review_json = g.db_connection.db_review_list_by_tmdb_guid(
            json_metaid['themoviedb'])
        if review_json is not None and len(review_json) > 0:
            review_json = review_json[0]
            for review_data in review_json[1]['themoviedb']['results']:
                review.append(
                    (review_data['author'], review_data['url'], review_data['content']))
        # do chapter stuff here so I can sort
        data_json_media_chapters = []
        try:
            for chap_data in natsort.natsorted(json_media['ChapterImages']):
                data_json_media_chapters.append((chap_data,
                                                 json_media['ChapterImages'][chap_data]))
        except:
            pass
        # set watched and sync
        try:
            watched_status = json_media['UserStats'][current_user.get_id()]['Watched']
        except:
            watched_status = False
        try:
            sync_status = json_media['Synced']
        except:
            sync_status = False
        return render_template('users/user_movie_detail.html', data=data[0],
                               json_media=json_media,
                               json_metadata=json_metadata,
                               data_genres=genres_list[:-2],
                               data_production=production_list[:-2],
                               data_budget=budget,
                               data_revenue=revenue,
                               data_guid=guid,
                               data_playback_url='/users/playvideo_videojs/hls/' + guid,
                               data_review=review,
                               data_poster_image=data_poster_image,
                               data_background_image=data_background_image,
                               data_vote_count=data_vote_count,
                               data_json_media_chapters=data_json_media_chapters,
                               data_watched_status=watched_status,
                               data_sync_status=sync_status,
                               data_runtime="%02dH:%02dM:%02dS" % (
                                   hours, minutes, seconds)
                               )


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
