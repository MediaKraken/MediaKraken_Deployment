"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from quart import Blueprint, render_template, g, request
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
from common import common_network_twitch
from common import common_network_youtube
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()

google_instance = common_google.CommonGoogle(option_config_json)


# internet sites
@blueprint.route('/internet')
@blueprint.route('/internet/')
@login_required
async def user_internet():
    """
    Display internet page
    """
    return await render_template("users/user_internet.html")


# youtube
@blueprint.route('/internet/internet_youtube', methods=["GET", "POST"])
@blueprint.route('/internet/internet_youtube/', methods=["GET", "POST"])
@login_required
async def user_internet_youtube():
    """
    Display youtube page
    """
    youtube_videos = []
    form = SearchForm(await request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
        videos, channels, playlists = google_instance.com_google_youtube_search(
            await request.form['search_text'])
        for url_link in videos:
            common_global.es_inst.com_elastic_index('info', {'searchurllink': url_link})
            youtube_videos.append(
                json.loads(google_instance.com_google_youtube_info(url_link, 'snippet')))
    else:
        # get trending for specified country code
        for url_link in common_network_youtube.com_net_yt_trending(locale.getdefaultlocale()[0]):
            common_global.es_inst.com_elastic_index('info', {'urllink': url_link})
            youtube_videos.append(json.loads(google_instance.com_google_youtube_info(url_link,
                                                                                     'snippet')))
    common_global.es_inst.com_elastic_index('info', {'temphold': youtube_videos})
    return await render_template("users/user_internet_youtube.html", form=form,
                           media=youtube_videos)


# youtube detail
@blueprint.route('/internet/youtube_detail/<uuid>')
@blueprint.route('/internet/youtube_detail/<uuid>/')
@login_required
async def user_internet_youtube_detail(uuid):
    """
    Display youtube details page
    """
    form = SearchForm(await request.form)
    return await render_template("users/user_internet_youtube_detail.html", form=form,
                           media=json.loads(
                               google_instance.com_google_youtube_info(uuid)),
                           data_guid=uuid)


# vimeo
@blueprint.route('/internet/internet_vimeo')
@blueprint.route('/internet/internet_vimeo/')
@login_required
async def user_internet_vimeo():
    """
    Display vimeo page
    """
    return await render_template("users/user_internet_vimeo.html")


# twitch tv
@blueprint.route('/internet/internet_twitch')
@blueprint.route('/internet/internet_twitch/')
@login_required
async def user_internet_twitch():
    """
    Display twitchtv page
    """
    twitch_api = common_network_twitch.CommonNetworkTwitch()
    twitch_media = []
    for stream_data in twitch_api.com_twitch_get_featured_streams()['featured']:
        common_global.es_inst.com_elastic_index('info', {"stream": stream_data})
        try:
            if stream_data['stream']['game'] is None:
                twitch_media.append((stream_data['stream']['name'],
                                     stream_data['stream']['preview']['medium'], 'Not Available'))
            else:
                twitch_media.append((stream_data['stream']['name'],
                                     stream_data['stream']['preview']['medium'],
                                     stream_data['stream']['game']))
        except:
            if stream_data['stream']['channel']['game'] is None:
                twitch_media.append((stream_data['stream']['channel']['name'],
                                     stream_data['stream']['preview']['medium'],
                                     'Not Available'))
            else:
                twitch_media.append((stream_data['stream']['channel']['name'],
                                     stream_data['stream']['preview']['medium'],
                                     stream_data['stream']['channel']['game']))
    return await render_template("users/user_internet_twitch.html", media=twitch_media)


# twitch tv detail on stream
@blueprint.route('/internet/internet_twitch_stream_detail/<stream_name>')
@blueprint.route('/internet/internet_twitch_stream_detail/<stream_name>/')
@login_required
async def user_internet_twitch_stream_detail(stream_name):
    """
    Show twitch stream detail page
    """
    # twitch_api = common_network_Twitch.com_Twitch_API()
    # media = twitch_api.com_Twitch_Channel_by_Name(stream_name)
    common_global.es_inst.com_elastic_index('info', {'twitch stream_name': stream_name})
    return await render_template("users/user_internet_twitch_stream_detail.html", media=stream_name)


# flickr
@blueprint.route('/internet/internet_flickr')
@blueprint.route('/internet/internet_flickr/')
@login_required
async def user_internet_flickr():
    """
    Display main page for flickr
    """
    return await render_template("users/user_internet_flickr.html")


# iradio
@blueprint.route('/iradio', methods=['GET', 'POST'])
@blueprint.route('/iradio/', methods=['GET', 'POST'])
@login_required
async def user_iradio_list():
    """
    Display main page for internet radio
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    form = SearchForm(await request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
        mediadata = g.db_connection.db_iradio_list(offset, per_page,
                                                   search_value=await request.form['search_text'])
    else:
        mediadata = g.db_connection.db_iradio_list(offset, per_page)

    return await render_template("users/user_iradio_list.html", form=form)


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
