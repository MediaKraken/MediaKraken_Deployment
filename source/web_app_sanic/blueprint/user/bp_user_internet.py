import json
import locale

from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_network_youtube
from sanic import Blueprint

blueprint_user_internet = Blueprint('name_blueprint_user_internet', url_prefix='/user')


@blueprint_user_internet.route('/user_internet', methods=['GET'])
@common_global.jinja_template.template('bss_user/internet/bss_user_internet.html')
@common_global.auth.login_required
async def url_bp_user_internet(request):
    """
    Display internet page
    """
    return {}


@blueprint_user_internet.route('/user_internet/flickr')
@common_global.jinja_template.template('bss_user/internet/bss_user_internet_flickr.html')
@common_global.auth.login_required
async def url_bp_user_internet_flickr(request):
    """
    Display main page for flickr
    """
    return {}


@blueprint_user_internet.route('/user_internet/internet/bss_user_internet_flickr_detail/<guid>')
@common_global.auth.login_required
async def url_bp_user_internet_flickr_detail(request, guid):
    """
    Display main page for flickr
    """
    return {}


@blueprint_user_internet.route('/user_internet/twitch')
@common_global.jinja_template.template('bss_user/internet/bss_user_internet_twitch.html')
@common_global.auth.login_required
async def url_bp_user_internet_twitch(request):
    """
    Display twitchtv page
    """
    twitch_media = []
    for stream_data in g.twitch_api.com_net_twitch_get_featured():
        pass

    # twitch_api = common_network_twitch.CommonNetworkTwitch()
    # twitch_media = []
    # for stream_data in twitch_api.com_twitch_get_featured_streams()['featured']:
    #     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {"stream": stream_data})
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
    return {
        'media': twitch_media
    }


@blueprint_user_internet.route('/user_internet/twitch_stream_detail/<stream_name>')
@common_global.jinja_template.template(
    'bss_user/internet/bss_user_internet_twitch_stream_detail.html')
@common_global.auth.login_required
async def url_bp_user_internet_twitch_stream_detail(request, stream_name):
    """
    Show twitch stream detail page
    """
    # twitch_api = common_network_Twitch.com_Twitch_API()
    # media = twitch_api.com_Twitch_Channel_by_Name(stream_name)
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'twitch stream_name': stream_name})
    return {
        'media': stream_name
    }


@blueprint_user_internet.route('/user_internet/vimeo')
@common_global.jinja_template.template('bss_user/internet/bss_user_internet_vimeo.html')
@common_global.auth.login_required
async def url_bp_user_internet_vimeo(request):
    """
    Display vimeo page
    """
    return {}


@blueprint_user_internet.route('/user_internet/internet/bss_user_internet_vimeo_detail/<guid>')
@common_global.auth.login_required
async def url_bp_user_internet_vimeo_detail(request, guid):
    """
    Display vimeo page
    """
    pass


@blueprint_user_internet.route('/user_internet/youtube', methods=["GET", "POST"])
@common_global.jinja_template.template('bss_user/internet/bss_user_internet_youtube.html')
@common_global.auth.login_required
async def url_bp_user_internet_youtube(request):
    """
    Display youtube page
    """
    youtube_videos = []
    if request.ctx.session['search_text'] is not None:
        videos, channels, playlists = g.google_instance.com_google_youtube_search(
            request.ctx.session['search_text'])
        for url_link in videos:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'searchurllink': url_link})
            youtube_videos.append(
                json.loads(g.google_instance.com_google_youtube_info(url_link, 'snippet')))
    else:
        # get trending for specified country code
        for url_link in common_network_youtube.com_net_yt_trending(locale.getdefaultlocale()[0]):
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                 message_text={'urllink': url_link})
            youtube_videos.append(json.loads(g.google_instance.com_google_youtube_info(url_link,
                                                                                       'snippet')))
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={'temphold': youtube_videos})
    return {
        'media': youtube_videos
    }


@blueprint_user_internet.route('/user_internet/youtube_detail/<uuid>')
@common_global.jinja_template.template('bss_user/internet/bss_user_internet_youtube_detail.html')
@common_global.auth.login_required
async def url_bp_user_internet_youtube_detail(request, uuid):
    """
    Display youtube details page
    """
    return {
        'media': json.loads(g.google_instance.com_google_youtube_info(uuid)),
        'data_guid': uuid
    }
