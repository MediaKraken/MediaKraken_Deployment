
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify, redirect, url_for
from flask_login import login_required
from flask_login import current_user
#from flask_table import Table, Col, create_table
from MediaKraken.user.forms import SyncEditForm
from flask_paginate import Pagination
from fractions import Fraction
blueprint = Blueprint("user", __name__, url_prefix='/users', static_folder="../static")


# import localization
import locale
locale.setlocale(locale.LC_ALL, '')

# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("../MediaKraken.ini")

import pygal
import logging
import datetime
import uuid
import json
import subprocess
import natsort
import os
import sys
sys.path.append('../')
import database as database_base
sys.path.append('../../MediaKraken_Common')
import MK_Common_File
import MK_Common_Google
import MK_Common_Network_Twitch
import MK_Common_Network_Vimeo
import MK_Common_Network_Youtube
import MK_Common_Pagination
import MK_Common_String


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@blueprint.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload_image():
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
    resume_list = []
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Read_Media_New_Count(7),
                                record_name='new and hot',
                                format_total=True,
                                format_number=True,
                                )
    return render_template("users/members.html", data_resume_media = resume_list,
                           data_new_media = g.db.MK_Server_Database_Read_Media_New(7, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


# internet sites
@blueprint.route('/internet')
@blueprint.route('/internet/')
@login_required
def user_internet():
    return render_template("users/user_internet.html")


# youtube
@blueprint.route('/internet/internet_youtube')
@blueprint.route('/internet/internet_youtube/')
@login_required
def user_internet_youtube():
    return render_template("users/user_internet_youtube.html", media=MK_Common_Google.MK_Common_Google_Youtube_Feed_List('top_rated'))


# vimeo
@blueprint.route('/internet/internet_vimeo')
@blueprint.route('/internet/internet_vimeo/')
@login_required
def user_internet_vimeo():
    return render_template("users/user_internet_vimeo.html")


# twitch tv
@blueprint.route('/internet/internet_twitch')
@blueprint.route('/internet/internet_twitch/')
@login_required
def user_internet_twitch():
    twitch_api = MK_Common_Network_Twitch.MK_Common_Twitch_API()
    twitch_media = []
    for stream_data in twitch_api.MK_Common_Twitch_Get_Featured_Streams()['featured']:
        logging.debug("stream: %s", stream_data)
        try:
            twitch_media.append((stream_data['stream']['name'], stream_data['stream']['preview']['medium'], stream_data['stream']['game']))
        except:
            twitch_media.append((stream_data['stream']['channel']['name'], stream_data['stream']['preview']['medium'], stream_data['stream']['channel']['game']))
    return render_template("users/user_internet_twitch.html", media=twitch_media)


# twitch tv detail on stream
@blueprint.route('/internet/internet_twitch_stream_detail/<stream_name>')
@blueprint.route('/internet/internet_twitch_stream_detail/<stream_name>/')
@login_required
def user_internet_twitch_stream_detail(stream_name):
    #twitch_api = MK_Common_Network_Twitch.MK_Common_Twitch_API()
    #media = twitch_api.MK_Common_Twitch_Channel_By_Name(stream_name)
    #logging.debug("str detail: %s", media)
    return render_template("users/user_internet_twitch_stream_detail.html", media=stream_name)


# flickr
@blueprint.route('/internet/internet_flickr')
@blueprint.route('/internet/internet_flickr/')
@login_required
def user_internet_flickr():
    return render_template("users/user_internet_flickr.html")


# home media
@blueprint.route('/home_media')
@blueprint.route('/home_media/')
@login_required
def user_home_media_list():
    return render_template("users/user_home_media_list.html")


# iradio
@blueprint.route('/iradio')
@blueprint.route('/iradio/')
@login_required
def user_iradio_list():
    return render_template("users/user_iradio_list.html")


# books
@blueprint.route('/books')
@blueprint.route('/books/')
@login_required
def user_books_list():
    return render_template("users/user_books_list.html")


# 3d
@blueprint.route('/3D')
@blueprint.route('/3D/')
@login_required
def user_3d_list():
    return render_template("users/user_3d_list.html")


@blueprint.route('/music_video_list')
@blueprint.route('/music_video_list/')
@login_required
def user_music_video_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Table_Count('mm_music_video'),
                                record_name='music video',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/user_music_video_list.html', media_person=g.db.MK_Server_Database_Music_Video_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


# list of spoting events
@blueprint.route("/sports")
@blueprint.route("/sports/")
@login_required
def user_sports_page():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    media = []
    for row_data in g.db.MK_Server_Database_Metadata_Sports_List(offset, per_page):
        media.append((row_data['mm_metadata_sports_guid'],row_data['mm_metadata_sports_name']))
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Metadata_Sports_List_Count(),
                                record_name='sporting events',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/user_sports_page.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route("/sports_detail/<guid>/", methods=['GET', 'POST'])
@blueprint.route("/sports_detail/<guid>", methods=['GET', 'POST'])
@login_required
def user_sports_detail_page(guid):
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # poster image
    try:
        if json_metadata['LocalImages']['Poster'] is not None:
            data_poster_image = json_metadata['LocalImages']['Poster'].replace(image_location,'')
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop'].replace(image_location,'')
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template("users/user_sports_detail.html", data=g.db.MK_Server_Database_MetadataTheSportsDB_Select_By_Guid(guid),
                           data_poster_image = data_poster_image,
                           data_background_image = data_background_image
                           )


# list of tv shows
@blueprint.route("/tv")
@blueprint.route("/tv/")
@login_required
def user_tv_page():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    # list_type, list_genre = None, list_limit = 500000, group_collection = False, offset = 0
    media = []
    for row_data in g.db.MK_Server_Database_Web_TVMedia_List('TV Show', None, per_page, False, offset):
        # 0 - mm_media_series_name, 1 - mm_media_series_guid, 2 - count(*), 3 - mm_metadata_tvshow_localimage_json
        try:
            media.append((row_data['mm_media_series_name'], row_data['mm_media_series_guid'], row_data['mm_metadata_tvshow_localimage_json'].replace(Config.get('MediaKrakenServer', 'MetadataImageLocal').strip(), ''), locale.format('%d', row_data['mm_count'], True)))
        except:
            media.append((row_data['mm_media_series_name'], row_data['mm_media_series_guid'], None, locale.format('%d', row_data['mm_count'], True)))
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Web_TVMedia_List_Count('TV Show', None, None),
                                record_name='media',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/user_tv_page.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


# tv show detail
@blueprint.route("/tv_show_detail/<guid>", methods=['GET', 'POST'])
@blueprint.route("/tv_show_detail/<guid>/", methods=['GET', 'POST'])
@login_required
def user_tv_show_detail_page(guid):
    if request.method == 'POST':
        # do NOT need to check for play video here, it's routed by the event itself in the html via the 'action' clause
        if request.form['status'] == 'Watched':
            g.db.MK_Server_Database_Media_Watched_Status_Update(guid,current_user.get_id(),False)
            return redirect(url_for('user.user_tv_show_detail_page', guid=guid))
        elif request.form['status'] == 'Unwatched':
            g.db.MK_Server_Database_Media_Watched_Status_Update(guid,current_user.get_id(),True)
            return redirect(url_for('user.user_tv_show_detail_page', guid=guid))
    else:
        # guid, name, id, metajson
        data_metadata = g.db.MK_Server_Database_Metadata_TVShow_Detail(guid)
        json_metadata = data_metadata['mm_metadata_tvshow_json']
        if 'TVMaze' in json_metadata['Meta']:
            if 'runtime' in json_metadata['Meta']['TVMaze']:
                data_runtime = json_metadata['Meta']['TVMaze']['runtime']
            else:
                data_runtime = None
            if 'rating' in json_metadata['Meta']['TVMaze']:
                data_rating = json_metadata['Meta']['TVMaze']['rating']['average']
            else:
                data_rating = None
            if 'premiered' in json_metadata['Meta']['TVMaze']:
                data_first_aired = json_metadata['Meta']['TVMaze']['premiered']
            else:
                data_first_aired = None
            if 'summary' in json_metadata['Meta']['TVMaze']:
                data_overview = json_metadata['Meta']['TVMaze']['summary'].replace('<p>','').replace('</p>','')
            else:
                data_overview = None
            # build gen list
            data_genres_list = u''
            if 'genres' in json_metadata['Meta']['TVMaze']:
                for ndx in json_metadata['Meta']['TVMaze']['genres']:
                    data_genres_list += (ndx + ', ')
        elif 'theTVDB' in json_metadata['Meta']:
            if 'Runtime' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
                data_runtime = json_metadata['Meta']['theTVDB']['Meta']['Series']['Runtime']
            else:
                data_runtime = None
            if 'ContentRating' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
                data_rating = json_metadata['Meta']['theTVDB']['Meta']['Series']['ContentRating']
            else:
                data_rating = None
            if 'FirstAired' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
                data_first_aired = json_metadata['Meta']['theTVDB']['Meta']['Series']['FirstAired']
            else:
                data_first_aired = None
            if 'Overview' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
                data_overview = json_metadata['Meta']['theTVDB']['Meta']['Series']['Overview']
            else:
                data_overview = None
            # build gen list
            data_genres_list = u''
            if 'Genre' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
                for ndx in json_metadata['Meta']['theTVDB']['Meta']['Series']['Genre'].split("|"):
                    data_genres_list += (ndx + ', ')
                # since | is at first and end....chop off first and last comma
                data_genres_list = data_genres_list[2:-2]

        # vote count format
        data_vote_count = 0 # locale.format('%d', json_metadata['vote_count'], True)

        # build production list
        production_list = u''
        #for ndx in range(0,len(json_metadata['production_companies'])):
        #    production_list += (json_metadata['production_companies'][ndx]['name'] + ', ')
        image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
        # poster image
        try:
            data_poster_image = data_metadata[3].replace(image_location, '')
        except:
            data_poster_image = None
        # background image
        try:
            if json_metadata['LocalImages']['Backdrop'] is not None:
                data_background_image = json_metadata['LocalImages']['Backdrop'].replace(image_location,'')
            else:
                data_background_image = None
        except:
            data_background_image = None
        # grab reviews
        #review = g.db.MK_Server_Database_Review_List(data[0])
        data_season_data = g.db.MK_Server_Database_Read_TVMetadata_Eps_Season(guid)
        data_season_count = sorted(data_season_data.iterkeys())
        # calculate a better runtime
        m, s = divmod((float(data_runtime) * 60), 60)
        h, m = divmod(m, 60)
        # set watched
        try:
            watched_status = json_media['UserStats'][current_user.get_id()]
        except:
            watched_status = False
        return render_template('users/user_tv_show_detail.html', data=data_metadata[0],
                                json_metadata=json_metadata,
                                data_genres=data_genres_list[:-2],
                                data_production=production_list[:-2],
                                data_image_local=image_location,
                                data_guid=guid,
                                data_overview = data_overview,
                                data_rating = data_rating,
                                data_first_aired = data_first_aired,
#                                data_review=review,
                                data_poster_image = data_poster_image,
                                data_background_image = data_background_image,
                                data_vote_count = data_vote_count,
                                data_watched_status = watched_status,
                                data_season_data = data_season_data,
                                data_season_count = data_season_count,
                                data_runtime = "%02dH:%02dM:%02dS" % (h, m, s)
                                )


# tv show season detail - show guid then season #
@blueprint.route("/tv_season_detail/<guid>/<season>", methods=['GET', 'POST'])
@blueprint.route("/tv_season_detail/<guid>/<season>/", methods=['GET', 'POST'])
@login_required
def user_tv_season_detail_page(guid, season):
    data_metadata = g.db.MK_Server_Database_Metadata_TVShow_Detail(guid)
    json_metadata = data_metadata['mm_metadata_tvshow_json']
    if 'TVMaze' in json_metadata['Meta']:
        if 'runtime' in json_metadata['Meta']['TVMaze']:
            data_runtime = json_metadata['Meta']['TVMaze']['runtime']
        else:
            data_runtime = None
        if 'rating' in json_metadata['Meta']['TVMaze']:
            data_rating = json_metadata['Meta']['TVMaze']['rating']['average']
        else:
            data_rating = None
        if 'premiered' in json_metadata['Meta']['TVMaze']:
            data_first_aired = json_metadata['Meta']['TVMaze']['premiered']
        else:
            data_first_aired = None
        if 'summary' in json_metadata['Meta']['TVMaze']:
            data_overview = json_metadata['Meta']['TVMaze']['summary'].replace('<p>','').replace('</p>','')
        else:
            data_overview = None
        # build gen list
        data_genres_list = u''
        if 'genres' in json_metadata['Meta']['TVMaze']:
            for ndx in json_metadata['Meta']['TVMaze']['genres']:
                data_genres_list += (ndx + ', ')
    elif 'theTVDB' in json_metadata['Meta']:
        if 'Runtime' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_runtime = json_metadata['Meta']['theTVDB']['Meta']['Series']['Runtime']
        else:
            data_runtime = None
        if 'ContentRating' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_rating = json_metadata['Meta']['theTVDB']['Meta']['Series']['ContentRating']
        else:
            data_rating = None
        if 'FirstAired' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_first_aired = json_metadata['Meta']['theTVDB']['Meta']['Series']['FirstAired']
        else:
            data_first_aired = None
        if 'Overview' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_overview = json_metadata['Meta']['theTVDB']['Meta']['Series']['Overview']
        else:
            data_overview = None
        # build gen list
        data_genres_list = u''
        if 'Genre' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            for ndx in json_metadata['Meta']['theTVDB']['Meta']['Series']['Genre'].split("|"):
                data_genres_list += (ndx + ', ')
            # since | is at first and end....chop off first and last comma
            data_genres_list = data_genres_list[2:-2]

    data_episode_count = g.db.MK_Server_Database_Read_TVMetadata_Season_Eps_List(guid, int(season))
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # poster image
    try:
        data_poster_image = data_metadata[3].replace(image_location, '')
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop'].replace(image_location,'')
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template("users/user_tv_season_detail.html", data=data_metadata[0],
                                data_guid=guid,
                                data_season=season,
                                data_overview = data_overview,
                                data_rating = data_rating,
                                data_first_aired = data_first_aired,
                                data_image_local=image_location,
                                data_poster_image = data_poster_image,
                                data_background_image = data_background_image,
                                data_episode_count=data_episode_count)


# tv show episode detail
@blueprint.route("/tv_episode_detail/<guid>/<season>/<episode>", methods=['GET', 'POST'])
@blueprint.route("/tv_episode_detail/<guid>/<season>/<episode>/", methods=['GET', 'POST'])
@login_required
def user_tv_episode_detail_page(guid, season, episode):
    data_episode_detail = g.db.MK_Server_Database_Read_TVMetadata_Episode(guid, season, episode)
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # poster image
    try:
        data_poster_image = data_metadata[3].replace(image_location, '')
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop'].replace(image_location,'')
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template("users/user_tv_episode_detail.html", data=data_episode_detail,
                                data_image_local=image_location,
                                data_poster_image = data_poster_image,
                                data_background_image = data_background_image)


# livetv list
@blueprint.route("/livetv/<schedule_date>/<schedule_time>")
@blueprint.route("/livetv/<schedule_date>/<schedule_time>/")
@login_required
def user_livetv_page(schedule_date, schedule_time):
    grid_data = '<table style="width:100%" border="2"></tr><th>Station</th><th>Channel</th>'
    for ndx in range(0,10):
        grid_data += '<th>' + str((int(schedule_time) + (30 * ndx))) + '</th>'
    grid_data += '</tr>'
    channel_data = ""
    md_used = 2
    last_station = None
    for row_data in g.db.MK_Server_Database_TV_Schedule_By_Date(schedule_date):
        if row_data[0] != last_station and last_station is not None:
            grid_data += '<tr><td>' + last_station + '</td><td>' + row_data[1] + '</td>' + channel_data + '</tr>'
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
                        audio_html += '<img src="../../../static/images/media_flags/caption-icon.png" alt="Closed Caption" style="width:15px;height:15px;">'
                    elif audio_features == "stereo":
                        audio_html += '<img src="../../../static/images/media_flags/audio_channels/2.png" alt="Stereo Sound" style="width:15px;height:15px;">'
                    elif audio_features == "DD 5.1":
                        audio_html += '<img src="../../../static/images/media_flags/audio_channels/6.png" alt="DD 5.1" style="width:15px;height:15px;">'
                    elif audio_features == "SAP":
                        audio_html += '<img src="../../../static/images/media_flags/sap-icon.png" alt="SAP" style="width:15px;height:15px;">'
                    elif audio_features == "dvs":
                        audio_html += '<img src="../../../static/images/media_flags/dvs-icon.png" alt="Descriptive Video Service" style="width:15px;height:15px;">'
                    elif audio_features == "DD":
                        audio_html += '<img src="../../../static/images/media_flags/audio_codec/dolby_digital.png" alt="Dolby Digital" style="width:15px;height:15px;">'
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
                        video_html += '<img src="../../../static/images/3D.png" alt="3D" style="width:15px;height:15px;">'
                    elif video_features == "hdtv":
                        video_html += '<img src="../../../static/images/media_flags/video_resolution.png" alt="HDTV" style="width:15px;height:15px;">'
# TODO
#    enhanced - Enhanced is better video quality than Standard Definition, but not true High Definition. (720p / 1080i)
#    letterbox
#    sdtv
#    uhdtv - the content is in "UHDTV"; this is provider-dependent and does not imply any particular resolution or encoding

            rating_html = ""
            if 'ratings' in row_data[2]:
                for rating_features in row_data[2]['ratings']:
                    if rating_features['code'] == "TVG":
                        rating_html += '<img src="../../../static/images/media_flags/content_rating/TV-G.png" alt="TV-G" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVY7":
                        rating_html += '<img src="../../../static/images/media_flags/content_rating/TV-Y7.png" alt="TV-Y7" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVY":
                        rating_html += '<img src="../../../static/images/media_flags/content_rating/TV-Y.png" alt="TV-Y" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVPG":
                        rating_html += '<img src="../../../static/images/media_flags/content_rating/TV-PG.png" alt="TV-PG" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TV14":
                        rating_html += '<img src="../../../static/images/media_flags/content_rating/TV-14.png" alt="TV-14" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVMA":
                        rating_html += '<img src="../../../static/images/media_flags/content_rating/TV-MA.png" alt="TV-MA" style="width:15px;height:15px;">'
            channel_data += '<td colspan="' + str(next_md) + '\">' + row_data[2]['programID'] + audio_html + rating_html + '</td>'
            md_used += next_md
    # populate last row
    grid_data += '<tr><td>' + last_station + '</td>' + channel_data + '</tr>'
    return render_template("users/user_livetv_page.html", media=grid_data)


# livetv list detail
@blueprint.route("/livetv_detail/<guid>/")
@blueprint.route("/livetv_detail/<guid>")
@login_required
def user_livetv_detail_page(guid):
    return render_template("users/user_livetv_page.html")


@blueprint.route('/playvideo/<guid>/')
@blueprint.route('/playvideo/<guid>')
@login_required
def user_video_player(guid):
    # grab the guid from the comboindex
    media_guid_index = request.form["Video_Track"]
    # call ffpmeg with the play_data
    audio_track_index = request.form["Video_Play_Audio_Track"]
    subtitle_track_index = request.form["Video_Play_Subtitles"]
    # launch ffmpeg to ffserver procecss
    proc_ffserver = subprocess.Popen(['ffmpeg', '-i', g.db.MK_Server_Database_Media_Path_By_UUID(media_guid_index)[0], 'http://localhost:8900/stream.ffm'], shell=False)
    logging.info("FFServer PID: %s",proc_ffserver.pid)
    return render_template("users/user_playback.html", data_desc = ('Movie title') )


@blueprint.route('/playvideo_videojs/<mtype>/<guid>/')
@blueprint.route('/playvideo_videojs/<mtype>/<guid>')
@login_required
def user_video_player_videojs(mtype, guid):
    logging.debug("videojs: %s %s", mtype, guid)
    # grab the guid from the comboindex
    media_guid_index = request.form["Video_Track"]
    media_path = g.db.MK_Server_Database_Media_Path_By_UUID(media_guid_index)[0]
    # set ffpmeg options with the play_data
    audio_track_index = request.form["Video_Play_Audio_Track"]
    logging.debug("aud: %s", audio_track_index)
    atracks=['-map ' + audio_track_index] # 0:0 as example
    subtitle_track_index = request.form["Video_Play_Subtitles"]
    logging.debug("sub: %s", subtitle_track_index)
    if subtitle_track_index is not None:
        subtracks = ['subtitles=' + media_path, 'language=' + subtitle_track_index]
    else:
        # TODO example from file
        subtracks = ['subtitles=subtitle.srt']
    # fire up ffmpeg process
    if mtype == "hls":
        vid_name = "./static/cache/" + str(uuid.uuid4()) + ".m3u8"
        acodecs=['aac', '-ac:a:0', '2', '-vbr', '5']
        p=subprocess.Popen(["ffmpeg", "-i", media_path, "-vcodec", "libx264", "-preset", "veryfast", "-acodec"] + acodecs + atracks + ["-vf"] + subtracks + ["yadif=0:0:0", vid_name], shell=False)
        logging.info("FFMPEG Pid: %s", p.pid)

#ffmpeg -i input.mp4 -profile:v baseline -level 3.0 -s 640x360 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls index.m3u8        

        pass_guid = 'http://10.0.0.179' + '/user/static/cache/' + vid_name
        #pass_guid = '//s3.amazonaws.com/_bc_dml/example-content/tears-of-steel/playlist.m3u8'
    else:
        pass_guid = guid
    logging.debug("hls path: %s", pass_guid)
    return render_template("users/user_playback_videojs.html", data_desc=('Movie title'),
                           data_guid=pass_guid,
                           data_mtype=mtype)


@blueprint.route('/playalbum/<guid>/')
@blueprint.route('/playalbum/<guid>')
@login_required
def user_album_player(guid):
    return render_template("users/user_album_playback.html", data_desc = g.db.MK_Server_Database_Metadata_Album_By_GUID(guid),
                           data_song_list = g.db.MK_Server_Database_Metadata_Songs_By_Album_GUID(guid))


@blueprint.route('/imagegallery')
@blueprint.route('/imagegallery/')
@login_required
def user_image_gallery():
    return render_template("users/user_image_gallery_view.html", image_data=g.db.MK_Common_Media_Images_List())


@blueprint.route('/games')
@blueprint.route('/games/')
@login_required
def user_games_list():
    return render_template("users/user_game_list.html")


@blueprint.route('/games_detail/<guid>/', methods=['GET', 'POST'])
@blueprint.route('/games_detail/<guid>', methods=['GET', 'POST'])
@login_required
def user_games_detail(guid):
    return render_template("users/user_game_detail.html")


@blueprint.route("/movie_genre")
@blueprint.route("/movie_genre/")
@login_required
def user_movie_genre_page():
    media = []
    for row_data in g.db.MK_Server_Database_Media_Movie_Count_By_Genre(g.db.MK_Server_Database_Media_UUID_By_Class('Movie')):
        media.append((row_data['gen']['name'], locale.format('%d', row_data[1], True), row_data[0]['name'] + ".png"))
    return render_template('users/user_movie_genre_page.html', media=sorted(media))


@blueprint.route("/movie/<genre>")
@blueprint.route("/movie/<genre>/")
@login_required
def user_movie_page(genre):
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    media = []
    image_location = Config.get('MediaKrakenServer', 'MetadataImageLocal').strip()
    for row_data in g.db.MK_Server_Database_Web_Media_List(g.db.MK_Server_Database_Media_UUID_By_Class('Movie'), list_type='movie', list_genre=genre, list_limit=per_page, group_collection=False, offset=offset, include_remote=True):
        # 0- mm_media_name, 1- mm_media_guid, 2- mm_media_json, 3- mm_metadata_json, 4 - mm_metadata_localimage_json
        logging.debug("row2: %s", row_data['mm_media_json'])
        json_image = row_data[mm_metadata_localimage_json]
        # set watched
        try:
            watched_status = row_data['mm_media_json']['UserStats'][current_user.get_id()]['Watched']
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
            favorite_status = row_data['mm_media_json']['UserStats'][current_user.get_id()]['Favorite']
        except:
            favorite_status = False
        # set mismatch
        try:
            match_status = json_media['MatchFlag']
        except:
            match_status = False
        logging.debug("status: %s %s %s %s %s", watched_status, sync_status, poo_status, favorite_status, match_status)
        if 'TMDB' in json_image['Images'] and 'Poster' in json_image['Images']['TMDB'] and json_image['Images']['TMDB']['Poster'] is not None:
            media.append((row_data[mm_media_name], row_data[mm_media_guid], json_image['Images']['TMDB']['Poster'].replace(image_location, ''), watched_status, sync_status, poo_status, favorite_status, match_status))
        else:
            media.append((row_data[mm_media_name], row_data[mm_media_guid], None, watched_status, sync_status, poo_status, favorite_status, match_status))
    total = g.db.MK_Server_Database_Web_Media_List_Count(g.db.MK_Server_Database_Media_UUID_By_Class('Movie'), list_type='movie', list_genre=genre, group_collection=False, include_remote=True)
    pagination = MK_Common_Pagination.get_pagination(page=page,
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


@blueprint.route('/movie_detail/<guid>/', methods=['GET', 'POST'])
@blueprint.route('/movie_detail/<guid>', methods=['GET', 'POST'])
@login_required
def movie_detail(guid):
    if request.method == 'POST':
        # do NOT need to check for play video here, it's routed by the event itself in the html via the 'action' clause
        if request.form['status'] == 'Watched':
            g.db.MK_Server_Database_Media_Watched_Status_Update(guid, current_user.get_id(), False)
            return redirect(url_for('user.movie_detail', guid=guid))
        elif request.form['status'] == 'Unwatched':
            g.db.MK_Server_Database_Media_Watched_Status_Update(guid, current_user.get_id(), True)
            return redirect(url_for('user.movie_detail', guid=guid))
        elif request.form['status'] == 'Sync':
            return redirect(url_for('user.sync_edit', guid=guid))
        elif request.form['status'] == 'Cast':
            # grab the guid from the comboindex
            media_guid_index = request.form["Video_Track"]
            # call ffpmeg with the play_data
            audio_track_index = request.form["Video_Play_Audio_Track"]
            subtitle_track_index = request.form["Video_Play_Subtitles"]
            # launch ffmpeg to ffserver procecss
            proc_ffserver = subprocess.Popen(['ffmpeg', '-i', g.db.MK_Server_Database_Media_Path_By_UUID(media_guid_index)[0], 'http://localhost:8900/stream.ffm'], shell=False)
            logging.info("FFServer PID: %s", proc_ffserver.pid)
            return redirect(url_for('user.movie_detail', guid=guid))
    else:
        data = g.db.MK_Server_Database_Read_Media_Metadata_Both(guid)
        json_ffmpeg = data['mm_media_ffprobe_json']
        json_media = data['mm_media_json']
        json_metadata = data['mm_metadata_json']
        json_imagedata = data['mm_metadata_localimage_json']
        json_metaid = data['mm_metadata_media_id']
        # vote count format
        data_vote_count = locale.format('%d', json_metadata['Meta']['TMDB']['Meta']['vote_count'], True)
        # build gen list
        genres_list = u''
        for ndx in range(0,len(json_metadata['Meta']['TMDB']['Meta']['genres'])):
            genres_list += (json_metadata['Meta']['TMDB']['Meta']['genres'][ndx]['name'] + ', ')
        # build production list
        production_list = u''
        for ndx in range(0,len(json_metadata['Meta']['TMDB']['Meta']['production_companies'])):
            production_list += (json_metadata['Meta']['TMDB']['Meta']['production_companies'][ndx]['name'] + ', ')
        # budget format
        budget = locale.format('%d', json_metadata['Meta']['TMDB']['Meta']['budget'], True)
        # revenue format
        revenue = locale.format('%d', json_metadata['Meta']['TMDB']['Meta']['revenue'], True)
        # not all files have ffmpeg that didn't fail
        if json_ffmpeg is None:
            aspect_ratio = "NA"
            bitrate = "NA"
            file_size = "NA"
            h = 0
            m = 0
            s = 0
            data_resolution = "NA"
            data_codec = "NA"
            data_file = "NA"
        else:
            # aspect ratio
            aspect_ratio = str(Fraction(json_ffmpeg['streams'][0]['width'],json_ffmpeg['streams'][0]['height'])).replace('/',':')
            # bitrate
            bitrate = MK_Common_String.bytes2human(float(json_ffmpeg['format']['bit_rate']))
            # file size
            file_size = MK_Common_String.bytes2human(float(json_ffmpeg['format']['size']))
            # calculate a better runtime
            m, s = divmod(float(json_ffmpeg['format']['duration']), 60)
            #m, s = divmod(json_metadata['runtime'], 60)
            h, m = divmod(m, 60)            
            data_resolution = str(json_ffmpeg['streams'][0]['width']) + 'x' + str(json_ffmpeg['streams'][0]['height'])
            data_codec = json_ffmpeg['streams'][0]['codec_name']
            data_file = json_ffmpeg['format']['filename']
        image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
        # check to see if there are other version of this video file (dvd, hddvd, etc)
        vid_versions = g.db.MK_Server_Database_Media_By_Metadata_Guid(data[1])  # metadata guid
        # audio and sub sreams
        audio_streams = []
        subtitle_streams = [(0,'None')]
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
                    stream_codec = stream_info['codec_long_name'].rsplit('(',1)[1].replace(')','') + ' - '
                except:
                    pass
                if stream_info['codec_type'] == 'audio':
                    audio_streams.append((len(audio_streams),(stream_codec + stream_language + stream_title)[:-3]))
                elif stream_info['codec_type'] == 'subtitle':
                    subtitle_streams.append((len(subtitle_streams), stream_language[:-2]))
        # poster image
        try:
            if json_imagedata['Images']['TMDB']['Poster'] is not None:
                data_poster_image = json_imagedata['Images']['TMDB']['Poster'].replace(image_location,'')
            else:
                data_poster_image = None
        except:
            data_poster_image = None
        # background image
        try:
            if json_imagedata['Images']['TMDB']['Backdrop'] is not None:
                data_background_image = json_imagedata['Images']['TMDB']['Backdrop'].replace(image_location,'')
            else:
                data_background_image = None
        except:
            data_background_image = None
        # grab reviews
        review = []
        review_json = g.db.MK_Server_Database_Review_List_By_TMDB_GUID(json_metaid['TMDB'])
        if review_json is not None and len(review_json) > 0:
            review_json = review_json[0]
            for review_data in review_json[1]['TMDB']['results']:
                review.append((review_data['author'], review_data['url'], review_data['content']))
        # do chapter stuff here so I can sort
        data_json_media_chapters = []
        try:
            for chap_data in natsort.natsorted(json_media['ChapterImages']):
                data_json_media_chapters.append((chap_data,json_media['ChapterImages'][chap_data]))
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
                                json_ffmpeg=json_ffmpeg,
                                json_media=json_media,
                                json_metadata=json_metadata,
                                data_resolution=data_resolution,
                                data_codec=data_codec,
                                data_genres=genres_list[:-2],
                                data_production=production_list[:-2],
                                data_budget=budget,
                                data_revenue=revenue,
                                data_file=data_file,
                                data_file_size=file_size,
                                data_bitrate=bitrate,
                                data_image_local=image_location,
                                data_guid=guid,
                                data_playback_url='/users/playvideo_videojs/hls/'+guid,
                                data_detail_url='/users/movie_detail/'+guid,
                                data_audio_track=audio_streams,
                                data_sub_track=subtitle_streams,
                                data_aspect=aspect_ratio,
                                data_review=review,
                                data_vid_versions = vid_versions,
                                data_poster_image = data_poster_image,
                                data_background_image = data_background_image,
                                data_vote_count = data_vote_count,
                                data_json_media_chapters = data_json_media_chapters,
                                data_watched_status = watched_status,
                                data_sync_status = sync_status,
                                data_cast = True,
                                data_runtime = "%02dH:%02dM:%02dS" % (h, m, s)
                                )


#@blueprint.route("/video")
#@blueprint.route("/video/")
#@login_required
#def user_video_page():
#    page, per_page, offset = MK_Common_Pagination.get_page_items()
#    media = []
#    # class_guid, list_type, list_genre = None, list_limit = 500000, group_collection = False, offset = 0
#    media.append((g.db.MK_Server_Database_Web_Media_List(xxxx, 'in_progress', None, per_page, False, offset))) # extra parans so adds list
#    total = g.db.MK_Server_Database_Web_Media_List_Count(xxxx, 'in_progress', None, False)
#    media.append((g.db.MK_Server_Database_Web_Media_List(xxxx, 'recent_addition', None, per_page, False, offset)))
#    total += g.db.MK_Server_Database_Web_Media_List_Count(xxxx, 'recent_addition', None, False)
#    media.append((g.db.MK_Server_Database_Web_Media_List(xxxx, 'video', None, per_page, False, offset)))
#    total += g.db.MK_Server_Database_Web_Media_List_Count(xxxx, 'video', None, False)
#    pagination = MK_Common_Pagination.get_pagination(page=page,
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
    return render_template("users/user_audio_page.html")


@blueprint.route("/album_list")
@blueprint.route("/album_list/")
@login_required
def user_album_list_page():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    media = []
    for row_data in g.db.MK_Server_Database_Media_Album_List(offset, per_page):
        try:
            media.append((row_data['mm_metadata_album_guid'], row_data['mm_metadata_album_name'], row_data['mm_metadata_album_json'].replace(Config.get('MediaKrakenServer', 'MetadataImageLocal').strip(), '')))
        except:
            media.append((row_data['mm_metadata_album_guid'], row_data['mm_metadata_album_name'], None))
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Media_Album_Count(),
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
    return render_template("users/user_media_list.html")


@blueprint.route('/server')
@blueprint.route('/server/')
@login_required
def server():
    return render_template("users/user_server.html")


@blueprint.route('/search/<name>/')
@blueprint.route('/search/<name>')
@login_required
def search(name):
    sql = 'select count(*) from users where name like ?'
    args = ('%{}%'.format(name), )
    g.cur.execute(sql, args)
    try:
        total = g.cur.fetchone()[0]
    except:
        total = 0
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    sql = 'select * from users where name like %s limit {}, {}'
    g.cur.execute(sql.format(offset, per_page), args)
    users = g.cur.fetchall()
    pagination = MK_Common_Pagination.get_pagination(page=page,
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
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            filename = os.path.join(app.config['UPLOAD_FOLDER'], "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            return jsonify({"success":True})


@blueprint.route('/sync')
@blueprint.route('/sync/')
@login_required
def sync_display_all():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    # 0 - mm_sync_guid uuid, 1 - mm_sync_path, 2 - mm_sync_path_to, 3 - mm_sync_options_json
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Sync_List_Count(),
                                record_name='Sync Jobs',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/user_sync.html', media_sync=g.db.MK_Server_Database_Sync_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/sync_edit/<guid>/', methods=['GET', 'POST'])
@blueprint.route('/sync_edit/<guid>', methods=['GET', 'POST'])
@login_required
def sync_edit(guid):
    if request.method == 'POST':
        sync_json = {"Type": request.form['target_type'], "Size": request.form['target_file_size'], 'Media GUID': guid, 'Options': {'VContainer': request.form['target_container'], 'VCodec': request.form['target_codec'], 'AudioChannels': request.form['target_audio_channels'], 'ACodec': request.form['target_audio_codec'], 'ASRate': request.form['target_sample_rate']}, 'Priority': request.form['target_priority'], 'Status': 'Scheduled', 'Progress': 0}
        g.db.MK_Server_Database_Sync_Insert(request.form['name'], request.form['target_output_path'], json.dumps(sync_json))
        g.db.MK_Server_Database_Commit()
        return redirect(url_for('user.movie_detail', guid=guid))
    form = SyncEditForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        pass
    return render_template('users/user_sync_edit.html', guid=guid, form=form )


@blueprint.route('/sync_delete',methods=["POST"])
@login_required
def admin_sync_delete_page():
    g.db.MK_Server_Database_Sync_Delete(request.form['id'])
    g.db.MK_Server_Database_Commit()
    return json.dumps({'status':'OK'})


@blueprint.route('/class')
@blueprint.route('/class/')
@login_required
def class_display_all():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Media_Class_List_Count(),
                                record_name='Media Class',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/user_media_class_list.html', media_class=g.db.MK_Server_Database_Media_Class_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/report_duplicate')
@blueprint.route('/report_duplicate/')
@login_required
def report_display_all_duplicates():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Media_Duplicate_Count(),
                                record_name='All Duplicate Media',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/reports/report_all_duplicate_media.html', media=g.db.MK_Server_Database_Media_Duplicate(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/report_duplicate_detail/<guid>/')
@blueprint.route('/report_duplicate_detail/<guid>')
@login_required
def report_display_all_duplicates_detail(guid):
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    media = []
    for media_data in g.db.MK_Server_Database_Media_Duplicate_Detail(guid, offset, per_page):
        logging.debug("media: %s", media_data['mm_media_ffprobe_json'])
        for stream_data in media_data['mm_media_ffprobe_json']['streams']:
            if stream_data['codec_type'] == 'video':
                media.append((media_data['mm_media_guid'], media_data['mm_media_path'], str(stream_data['width']) + 'x' + str(stream_data['height']), media_data['mm_media_ffprobe_json']['format']['duration']))
                break
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Media_Duplicate_Detail_Count(guid)[0],
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
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    media_data = []
    for row_data in g.db.MK_Server_Database_Known_Media(offset, per_page):
        media_data.append((row_data['mm_media_path'], MK_Common_String.bytes2human(os.path.getsize(row_data['mm_media_path']))))
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Known_Media_Count(),
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
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Web_Media_List_Count(g.db.MK_Server_Database_Media_UUID_By_Class('Movie')),
                                record_name='Known Videos',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/reports/report_all_known_media_video.html', media=g.db.MK_Server_Database_Web_Media_List(g.db.MK_Server_Database_Media_UUID_By_Class('Movie'), offset=offset, list_limit=per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/report_top10/<mtype>')
@blueprint.route('/report_top10/<mtype>/')
@login_required
def report_top10(mtype):
    top10_data = None
    if mtype == '1': # all time
        top10_data = g.db.MK_Server_Database_Usage_Top10_AllTime()
    elif mtype == '2': # movie
        top10_data = g.db.MK_Server_Database_Usage_Top10_Movie()
    elif mtype == '3': # tv show
        top10_data = g.db.MK_Server_Database_Usage_Top10_TV_Show()
    elif mtype == '4': # tv episode
        top10_data = g.db.MK_Server_Database_Usage_Top10_TV_Episode()
    return render_template('users/reports/report_top10_base.html', media=top10_data)


@blueprint.route('/meta_person_detail/<guid>/')
@blueprint.route('/meta_person_detail/<guid>')
@login_required
def metadata_person_detail(guid):
    meta_data = g.db.MK_Server_Database_Metadata_Person_By_GUID(guid)
    json_metadata = meta_data['mmp_person_meta_json']
    json_imagedata = meta_data['mmp_person_image']
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # person image
    try:
        if json_imagedata['Images']['Poster'] is not None:
            data_person_image = "../../static/meta/images/" + json_imagedata['Images']['Poster'].replace(image_location,'').replace('../','')
        else:
            data_person_image = None
    except:
        data_person_image = None
    # also appears in
    meta_also_media = g.db.MK_Server_Database_Metadata_Person_As_Seen_In(meta_data[0])
    return render_template('users/metadata/meta_people_detail.html',
                           json_metadata=json_metadata,
                           data_person_image = data_person_image,
                           data_also_media = meta_also_media,
                           data_image_local=image_location
                           )


@blueprint.route('/meta_person_list')
@blueprint.route('/meta_person_list/')
@login_required
def metadata_person_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Table_Count('mm_metadata_person'),
                                record_name='People',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_people_list.html', media_person=g.db.MK_Server_Database_Metadata_Person_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/metadata_music_list')
@blueprint.route('/metadata_music_list/')
@login_required
def metadata_music_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Table_Count('mm_metadata_music'),
                                record_name='music',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_music_list.html', media_person=g.db.MK_Server_Database_Metadata_Music_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/metadata_music_video_list')
@blueprint.route('/metadata_music_video_list/')
@login_required
def metadata_music_video_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Table_Count('mm_metadata_music_video'),
                                record_name='music video',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_music_video_list.html', media_person=g.db.MK_Server_Database_Metadata_Music_Video_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/metadata_music_album_list')
@blueprint.route('/metadata_music_album_list/')
@login_required
def metadata_music_album_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Table_Count('mm_metadata_music_album'),
                                record_name='music album',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_music_album_list.html', media_person=g.db.MK_Server_Database_Metadata_Music_Album_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_movie_detail/<guid>/')
@blueprint.route('/meta_movie_detail/<guid>')
@login_required
def metadata_movie_detail(guid):
    data = g.db.MK_Server_Database_Read_Media_Metadata(guid)
    json_metadata = data['mm_metadata_json']
    json_imagedata = data['mm_metadata_localimage_json']
    # vote count format
    data_vote_count = locale.format('%d', json_metadata['Meta']['TMDB']['Meta']['vote_count'], True)
    # build gen list
    genres_list = u''
    for ndx in range(0,len(json_metadata['Meta']['TMDB']['Meta']['genres'])):
        genres_list += (json_metadata['Meta']['TMDB']['Meta']['genres'][ndx]['name'] + ', ')
    # build production list
    production_list = u''
    for ndx in range(0,len(json_metadata['Meta']['TMDB']['Meta']['production_companies'])):
        production_list += (json_metadata['Meta']['TMDB']['Meta']['production_companies'][ndx]['name'] + ', ')
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # poster image
    try:
        if json_imagedata['Images']['TMDB']['Poster'] is not None:
            data_poster_image = json_imagedata['Images']['TMDB']['Poster'].replace(image_location,'')
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_imagedata['Images']['TMDB']['Backdrop'] is not None:
            data_background_image = json_imagedata['Images']['TMDB']['Backdrop'].replace(image_location,'')
        else:
            data_background_image = None
    except:
        data_background_image = None
    # grab reviews
#    review = g.db.MK_Server_Database_Review_List(data[1])
    return render_template('users/metadata/meta_movie_detail.html',
#                                data_media_ids=data[1],
                                data_image_local=image_location,
                                data_name=data[2],
                                json_metadata=json_metadata,
                                data_genres=genres_list[:-2],
                                data_production=production_list[:-2],
#                                data_review=review,
                                data_poster_image = data_poster_image,
                                data_background_image = data_background_image,
                                data_vote_count = data_vote_count,
                                data_budget=locale.format('%d', json_metadata['Meta']['TMDB']['Meta']['budget'], True))


@blueprint.route('/meta_movie_list')
@blueprint.route('/meta_movie_list/')
@login_required
def metadata_movie_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Table_Count('mm_metadata_movie'),
                                record_name='Movies',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_movie_list.html', media_movie=g.db.MK_Server_Database_Metadata_Movie_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           image_location=Config.get('MediaKrakenServer','MetadataImageLocal').strip(),
                           )


@blueprint.route('/metadata_movie_collection_list')
@blueprint.route('/metadata_movie_collection_list/')
@login_required
def metadata_movie_collection_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    media = []
    for row_data in g.db.MK_Server_Database_Collection_List(offset, per_page):
        try:
            media.append((row_data['mm_metadata_collection_guid'],row_data['mm_metadata_collection_name'],row_data['mm_metadata_collection_imagelocal_json']['Poster'].replace(Config.get('MediaKrakenServer','MetadataImageLocal').strip(),'')))
        except:
            media.append((row_data['mm_metadata_collection_guid'],row_data['mm_metadata_collection_name'],None))
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Table_Count('mm_metadata_collection'),
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
    data_metadata = g.db.MK_Server_Database_Collection_Read_By_GUID(guid)
    json_metadata = data_metadata['mm_metadata_collection_json']
    json_imagedata = data_metadata['mm_metadata_collection_imagelocal_json']
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # poster image
    try:
        if json_imagedata['Poster'] is not None:
            data_poster_image = json_imagedata['Poster'].replace(image_location,'')
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_imagedata['Backdrop'] is not None:
            data_background_image = json_imagedata['Backdrop'].replace(image_location,'')
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template('users/metadata/meta_movie_collection_detail.html',
                            data_name=json_metadata['name'],
                            data_poster_image = data_poster_image,
                            data_background_image = data_background_image,
                            json_metadata=json_metadata
                            )


@blueprint.route('/meta_tvshow_detail/<guid>/')
@blueprint.route('/meta_tvshow_detail/<guid>')
@login_required
def metadata_tvshow_detail(guid):
    data_metadata = g.db.MK_Server_Database_Metadata_TVShow_Detail(guid)
    json_metadata = data_metadata['mm_metadata_tvshow_json']
    if 'TVMaze' in json_metadata['Meta']:
        if 'runtime' in json_metadata['Meta']['TVMaze']:
            data_runtime = json_metadata['Meta']['TVMaze']['runtime']
        else:
            data_runtime = None
        if 'rating' in json_metadata['Meta']['TVMaze']:
            data_rating = json_metadata['Meta']['TVMaze']['rating']['average']
        else:
            data_rating = None
        if 'premiered' in json_metadata['Meta']['TVMaze']:
            data_first_aired = json_metadata['Meta']['TVMaze']['premiered']
        else:
            data_first_aired = None
        if 'summary' in json_metadata['Meta']['TVMaze']:
            data_overview = json_metadata['Meta']['TVMaze']['summary'].replace('<p>','').replace('</p>','')
        else:
            data_overview = None
        # build gen list
        data_genres_list = u''
        if 'genres' in json_metadata['Meta']['TVMaze']:
            for ndx in json_metadata['Meta']['TVMaze']['genres']:
                data_genres_list += (ndx + ', ')
    elif 'theTVDB' in json_metadata['Meta']:
        if 'Runtime' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_runtime = json_metadata['Meta']['theTVDB']['Meta']['Series']['Runtime']
        else:
            data_runtime = None
        if 'ContentRating' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_rating = json_metadata['Meta']['theTVDB']['Meta']['Series']['ContentRating']
        else:
            data_rating = None
        if 'FirstAired' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_first_aired = json_metadata['Meta']['theTVDB']['Meta']['Series']['FirstAired']
        else:
            data_first_aired = None
        if 'Overview' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_overview = json_metadata['Meta']['theTVDB']['Meta']['Series']['Overview']
        else:
            data_overview = None
        # build gen list
        data_genres_list = u''
        if 'Genre' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            for ndx in json_metadata['Meta']['theTVDB']['Meta']['Series']['Genre'].split("|"):
                data_genres_list += (ndx + ', ')
            # since | is at first and end....chop off first and last comma
            data_genres_list = data_genres_list[2:-2]
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # poster image
    try:
        data_poster_image = data_metadata[3].replace(image_location, '')
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop'].replace(image_location,'')
        else:
            data_background_image = None
    except:
        data_background_image = None
    data_season_data = g.db.MK_Server_Database_Read_TVMetadata_Eps_Season(guid)
#    # build production list
#    production_list = u''
#    for ndx in range(0,len(json_metadata['production_companies'])):
#        production_list += (json_metadata['production_companies'][ndx]['name'] + ', ')
    return render_template('users/metadata/meta_tvshow_detail.html',
                            data_title=data_metadata['mm_metadata_tvshow_name'],
                            data_runtime=data_runtime,
                            data_guid=guid,
                            data_rating=data_rating,
                            data_first_aired=data_first_aired,
                            data_poster_image = data_poster_image,
                            data_background_image = data_background_image,
                            data_overview=data_overview,
                            data_season_data = data_season_data,
                            data_season_count = sorted(data_season_data.iterkeys()),
                            data_genres_list=data_genres_list[:-2]
                            )


# tv show season detail - show guid then season #
@blueprint.route("/meta_tvshow_season_detail/<guid>/<season>", methods=['GET', 'POST'])
@blueprint.route("/meta_tvshow_season_detail/<guid>/<season>/", methods=['GET', 'POST'])
@login_required
def metadata_tvshow_season_detail_page(guid, season):
    data_metadata = g.db.MK_Server_Database_Metadata_TVShow_Detail(guid)
    json_metadata = data_metadata['mm_metadata_tvshow_json']
    if 'TVMaze' in json_metadata['Meta']:
        if 'runtime' in json_metadata['Meta']['TVMaze']:
            data_runtime = json_metadata['Meta']['TVMaze']['runtime']
        else:
            data_runtime = None
        if 'rating' in json_metadata['Meta']['TVMaze']:
            data_rating = json_metadata['Meta']['TVMaze']['rating']['average']
        else:
            data_rating = None
        if 'premiered' in json_metadata['Meta']['TVMaze']:
            data_first_aired = json_metadata['Meta']['TVMaze']['premiered']
        else:
            data_first_aired = None
        if 'summary' in json_metadata['Meta']['TVMaze']:
            data_overview = json_metadata['Meta']['TVMaze']['summary'].replace('<p>','').replace('</p>','')
        else:
            data_overview = None
        # build gen list
        data_genres_list = u''
        if 'genres' in json_metadata['Meta']['TVMaze']:
            for ndx in json_metadata['Meta']['TVMaze']['genres']:
                data_genres_list += (ndx + ', ')
    elif 'theTVDB' in json_metadata['Meta']:
        if 'Runtime' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_runtime = json_metadata['Meta']['theTVDB']['Meta']['Series']['Runtime']
        else:
            data_runtime = None
        if 'ContentRating' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_rating = json_metadata['Meta']['theTVDB']['Meta']['Series']['ContentRating']
        else:
            data_rating = None
        if 'FirstAired' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_first_aired = json_metadata['Meta']['theTVDB']['Meta']['Series']['FirstAired']
        else:
            data_first_aired = None
        if 'Overview' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            data_overview = json_metadata['Meta']['theTVDB']['Meta']['Series']['Overview']
        else:
            data_overview = None
        # build gen list
        data_genres_list = u''
        if 'Genre' in json_metadata['Meta']['theTVDB']['Meta']['Series']:
            for ndx in json_metadata['Meta']['theTVDB']['Meta']['Series']['Genre'].split("|"):
                data_genres_list += (ndx + ', ')
            # since | is at first and end....chop off first and last comma
            data_genres_list = data_genres_list[2:-2]
    data_episode_count = g.db.MK_Server_Database_Read_TVMetadata_Season_Eps_List(guid, int(season))
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # poster image
    try:
        data_poster_image = data_metadata[3].replace(image_location, '')
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop'].replace(image_location,'')
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template("users/metadata/meta_tvshow_season_detail.html", data=data_metadata['mm_metadata_tvshow_name'],
                                data_guid=guid,
                                data_season=season,
                                data_overview = data_overview,
                                data_rating = data_rating,
                                data_first_aired = data_first_aired,
                                data_image_local=image_location,
                                data_poster_image = data_poster_image,
                                data_background_image = data_background_image,
                                data_episode_count=data_episode_count)


# tv show season detail - show guid then season #
@blueprint.route("/meta_tvshow_episode_detail/<guid>/<season>/<episode>", methods=['GET', 'POST'])
@blueprint.route("/meta_tvshow_episode_detail/<guid>/<season>/<episode>/", methods=['GET', 'POST'])
@login_required
def metadata_tvshow_episode_detail_page(guid, season, episode):
    data_metadata = g.db.MK_Server_Database_Read_TVMetadata_Episode(guid, season, episode)
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    # poster image
    try:
        data_poster_image = data_metadata[3].replace(image_location, '')  # TODO dictcursor
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop'].replace(image_location,'')
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template("users/metadata/meta_tvshow_episode_detail.html", data=data_metadata[0],
                                data_guid=guid,
                                data_title=data_metadata[2],
                                data_runtime=data_metadata[4],
                                data_season=season,
                                data_episode=episode,
                                data_overview=data_metadata[5],
                                data_first_aired=data_metadata[3],
                                data_image_local=image_location,
                                data_poster_image=data_poster_image,
                                data_background_image=data_background_image
                                )


@blueprint.route('/meta_tvshow_list')
@blueprint.route('/meta_tvshow_list/')
@login_required
def metadata_tvshow_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    media_tvshow = []
    image_location = Config.get('MediaKrakenServer','MetadataImageLocal').strip()
    for row_data in g.db.MK_Server_Database_Metadata_TVShow_List(offset, per_page):
        image_data = row_data[3]  # TODO json dictcursor
        try:
            image_data = image_data.replace(image_location,'')
        except:
            pass
        media_tvshow.append((row_data['mm_metadata_tvshow_guid'], row_data['mm_metadata_tvshow_name'], row_data[2], image_data))  # TODO dictcursor
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Metadata_TVShow_List_Count(),
                                record_name='TV Shows',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_tvshow_list.html', media_tvshow=media_tvshow,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_game_list')
@blueprint.route('/meta_game_list/')
@login_required
def metadata_game_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Table_Count('mm_metadata_game_software_info'),
                                record_name='Games',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_game_list.html', media_game=g.db.MK_Server_Database_Metadata_Game_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_game_detail/<guid>/')
@blueprint.route('/meta_game_detail/<guid>')
@login_required
def metadata_game_detail(guid):
    return render_template('users/metadata/meta_game_detail.html', guid=guid,
                               data=g.db.MK_Server_Database_Metadata_Game_By_GUID(guid)['gi_game_info_json'],
                               data_review=None)


@blueprint.route('/meta_game_system_list')
@blueprint.route('/meta_game_system_list/')
@login_required
def metadata_game_system_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Metadata_Game_System_List_Count(),
                                record_name='Game Systems',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_game_system_list.html', media_game_system=g.db.MK_Server_Database_Metadata_Game_System_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_game_system_detail/<guid>/')
@blueprint.route('/meta_game_system_detail/<guid>')
@login_required
def metadata_game_system_detail(guid):
    return render_template('users/metadata/meta_game_system_detail.html', guid=guid,
                           data=g.db.MK_Server_Database_Metadata_Game_System_By_GUID(guid))


@blueprint.route('/meta_sports_list')
@blueprint.route('/meta_sports_list/')
@login_required
def metadata_sports_list():
    page, per_page, offset = MK_Common_Pagination.get_page_items()
    pagination = MK_Common_Pagination.get_pagination(page=page,
                                per_page=per_page,
                                total=g.db.MK_Server_Database_Metadata_Sports_List_Count(),
                                record_name='sporting events',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('users/metadata/meta_sports_list.html', media_sports_list=g.db.MK_Server_Database_Metadata_Sports_List(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_sports_detail/<guid>/')
@blueprint.route('/meta_sports_detail/<guid>')
@login_required
def metadata_sports_detail(guid):
    return render_template('users/metadata/meta_sports_detail.html', guid=guid,
                           data=g.db.MK_Server_Database_Metadata_Sports_By_GUID(guid))


@blueprint.route('/media_status/<guid>/<media_type>/<event_type>/', methods=['GET', 'POST'])
@blueprint.route('/media_status/<guid>/<media_type>/<event_type>', methods=['GET', 'POST'])
@login_required
def media_status(guid, media_type, event_type):
    logging.debug('media status: %s %s %s', guid, media_type, event_type)
    if media_type == "movie":
        if event_type == "watched":
            g.db.MK_Server_Database_Media_Watched_Status_Update(guid, current_user.get_id(), True)
            return json.dumps({'status':'OK'})
        elif event_type == "sync":
            return redirect(url_for('user.sync_edit', guid=guid))
        elif event_type == "favorite":
            g.db.MK_Server_Database_Media_Favorite_Status_Update(guid, current_user.get_id(), True)
            return json.dumps({'status':'OK'})
        elif event_type == "poo":
            g.db.MK_Server_Database_Media_Poo_Status_Update(guid, current_user.get_id(), True)
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
    g.db = database_base.MK_Server_Database()
    g.db.MK_Server_Database_Open(Config.get('DB Connections','PostDBHost').strip(),Config.get('DB Connections','PostDBPort').strip(),Config.get('DB Connections','PostDBName').strip(),Config.get('DB Connections','PostDBUser').strip(),Config.get('DB Connections','PostDBPass').strip())


@blueprint.teardown_request
def teardown_request(exception):
    g.db.MK_Server_Database_Close()
