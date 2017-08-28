"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
blueprint = Blueprint("user_internet", __name__, url_prefix='/users', static_folder="../static")
import logging # pylint: disable=W0611
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_google
from common import common_network_twitch
from common import common_network_vimeo
from common import common_network_youtube
from common import common_pagination
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()

google_instance = common_google.CommonGoogle(option_config_json)

# internet sites
@blueprint.route('/internet')
@blueprint.route('/internet/')
@login_required
def user_internet():
    """
    Display internet page
    """
    return render_template("users/user_internet.html")


# youtube
@blueprint.route('/internet/internet_youtube')
@blueprint.route('/internet/internet_youtube/')
@login_required
def user_internet_youtube():
    """
    Display youtube page
    """
    # TODO pass country
    youtube_videos = []
    for url_link in common_network_youtube.com_net_yt_trending():
        logging.info('urllink: %s', url_link)
        youtube_videos.append(google_instance.com_google_youtube_info(url_link))
    logging.info('temphold: %s', youtube_videos)
    return render_template("users/user_internet_youtube.html",
        media=youtube_videos)


# vimeo
@blueprint.route('/internet/internet_vimeo')
@blueprint.route('/internet/internet_vimeo/')
@login_required
def user_internet_vimeo():
    """
    Display vimeo page
    """
    return render_template("users/user_internet_vimeo.html")


# twitch tv
@blueprint.route('/internet/internet_twitch')
@blueprint.route('/internet/internet_twitch/')
@login_required
def user_internet_twitch():
    """
    Display twitchtv page
    """
    twitch_api = common_network_twitch.CommonNetworkTwitch()
    twitch_media = []
    for stream_data in twitch_api.com_twitch_get_featured_streams()['featured']:
        logging.info("stream: %s", stream_data)
        try:
            if stream_data['stream']['game'] is None:
                twitch_media.append((stream_data['stream']['name'],
                    stream_data['stream']['preview']['medium'], 'Not Available'))
            else:
                twitch_media.append((stream_data['stream']['name'],
                    stream_data['stream']['preview']['medium'], stream_data['stream']['game']))
        except:
            if stream_data['stream']['channel']['game'] is None:
                twitch_media.append((stream_data['stream']['channel']['name'],
                    stream_data['stream']['preview']['medium'],
                    'Not Available'))
            else:
                twitch_media.append((stream_data['stream']['channel']['name'],
                    stream_data['stream']['preview']['medium'],
                    stream_data['stream']['channel']['game']))
    return render_template("users/user_internet_twitch.html", media=twitch_media)


# twitch tv detail on stream
@blueprint.route('/internet/internet_twitch_stream_detail/<stream_name>')
@blueprint.route('/internet/internet_twitch_stream_detail/<stream_name>/')
@login_required
def user_internet_twitch_stream_detail(stream_name):
    """
    Show twitch stream detail page
    """
    #twitch_api = common_network_Twitch.com_Twitch_API()
    #media = twitch_api.com_Twitch_Channel_by_Name(stream_name)
    #logging.info("str detail: %s", media)
    return render_template("users/user_internet_twitch_stream_detail.html", media=stream_name)


# flickr
@blueprint.route('/internet/internet_flickr')
@blueprint.route('/internet/internet_flickr/')
@login_required
def user_internet_flickr():
    """
    Display main page for flickr
    """
    return render_template("users/user_internet_flickr.html")


# iradio
@blueprint.route('/iradio')
@blueprint.route('/iradio/')
@login_required
def user_iradio_list():
    """
    Display main page for internet radio
    """
    return render_template("users/user_iradio_list.html")


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
