"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_internet", __name__, url_prefix='/users',
                      static_folder="../static")
import locale
import json
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_google
from common import common_network_twitchv5
from common import common_network_youtube
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()

google_instance = common_google.CommonGoogle(option_config_json)


# internet sites
@blueprint.route('/internet')
@login_required
def user_internet():
    """
    Display internet page
    """
    return render_template("users/user_internet.html")


# youtube
@blueprint.route('/internet/internet_youtube', methods=["GET", "POST"])
@login_required
def user_internet_youtube():
    """
    Display youtube page
    """
    youtube_videos = []
    if session['search_text'] is not None:
        videos, channels, playlists = google_instance.com_google_youtube_search(
            session['search_text'])
        for url_link in videos:
            common_global.es_inst.com_elastic_index('info', {'searchurllink': url_link})
            youtube_videos.append(
                json.loads(google_instance.com_google_youtube_info(url_link, 'snippet')))
        session['search_text'] = None
    else:
        # get trending for specified country code
        for url_link in common_network_youtube.com_net_yt_trending(locale.getdefaultlocale()[0]):
            common_global.es_inst.com_elastic_index('info', {'urllink': url_link})
            youtube_videos.append(json.loads(google_instance.com_google_youtube_info(url_link,
                                                                                     'snippet')))
    common_global.es_inst.com_elastic_index('info', {'temphold': youtube_videos})
    return render_template("users/user_internet_youtube.html",
                           media=youtube_videos)


# youtube detail
@blueprint.route('/internet/youtube_detail/<uuid>')
@login_required
def user_internet_youtube_detail(uuid):
    """
    Display youtube details page
    """
    return render_template("users/user_internet_youtube_detail.html",
                           media=json.loads(
                               google_instance.com_google_youtube_info(uuid)),
                           data_guid=uuid)


# vimeo
@blueprint.route('/internet/internet_vimeo')
@login_required
def user_internet_vimeo():
    """
    Display vimeo page
    """
    return render_template("users/user_internet_vimeo.html")


@blueprint.route('/internet/internet_vimeo_detail/<guid>')
@login_required
def user_internet_vimeo_detail(guid):
    """
    Display vimeo page
    """
    pass


# twitch tv
@blueprint.route('/internet/internet_twitch')
@login_required
def user_internet_twitch():
    """
    Display twitchtv page
    """
    twitch_api = common_network_twitchv5.CommonNetworkTwitchV5(option_config_json)
    twitch_media = []
    for stream_data in twitch_api.com_net_twitch_get_featured():
        pass

    # twitch_api = common_network_twitch.CommonNetworkTwitch()
    # twitch_media = []
    # for stream_data in twitch_api.com_twitch_get_featured_streams()['featured']:
    #     common_global.es_inst.com_elastic_index('info', {"stream": stream_data})
    #     try:
    #         if stream_data['stream']['game'] is None:
    #             twitch_media.append((stream_data['stream']['name'],
    #                                  stream_data['stream']['preview']['medium'], 'Not Available'))
    #         else:
    #             twitch_media.append((stream_data['stream']['name'],
    #                                  stream_data['stream']['preview']['medium'],
    #                                  stream_data['stream']['game']))
    #     except:
    #         if stream_data['stream']['channel']['game'] is None:
    #             twitch_media.append((stream_data['stream']['channel']['name'],
    #                                  stream_data['stream']['preview']['medium'],
    #                                  'Not Available'))
    #         else:
    #             twitch_media.append((stream_data['stream']['channel']['name'],
    #                                  stream_data['stream']['preview']['medium'],
    #                                  stream_data['stream']['channel']['game']))
    return render_template("users/user_internet_twitch.html", media=twitch_media)


# twitch tv detail on stream
@blueprint.route('/internet/internet_twitch_stream_detail/<stream_name>')
@login_required
def user_internet_twitch_stream_detail(stream_name):
    """
    Show twitch stream detail page
    """
    # twitch_api = common_network_Twitch.com_Twitch_API()
    # media = twitch_api.com_Twitch_Channel_by_Name(stream_name)
    common_global.es_inst.com_elastic_index('info', {'twitch stream_name': stream_name})
    return render_template("users/user_internet_twitch_stream_detail.html", media=stream_name)


# flickr
@blueprint.route('/internet/internet_flickr')
@login_required
def user_internet_flickr():
    """
    Display main page for flickr
    """
    return render_template("users/user_internet_flickr.html")


@blueprint.route('/internet/internet_flickr_detail/<guid>')
@login_required
def user_internet_flickr_detail(guid):
    """
    Display main page for flickr
    """
    pass


# iradio
@blueprint.route('/iradio', methods=['GET', 'POST'])
@login_required
def user_iradio_list():
    """
    Display main page for internet radio
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    if session['search_text'] is not None:
        mediadata = g.db_connection.db_iradio_list(offset, per_page,
                                                   search_value=session['search_text'])
        session['search_text'] = None
    else:
        mediadata = g.db_connection.db_iradio_list(offset, per_page)
    return render_template("users/user_iradio_list.html")


@blueprint.route('/iradio_detail/<guid>')
@login_required
def user_iradio_detail(guid):
    """
    Display main page for internet radio
    """
    pass


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
