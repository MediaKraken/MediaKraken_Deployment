import locale

from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_network_youtube
from sanic import Blueprint

blueprint_user_internet_youtube = Blueprint('name_blueprint_user_internet_youtube',
                                            url_prefix='/user')


@blueprint_user_internet_youtube.route('/user_internet/youtube', methods=["GET", "POST"])
@common_global.jinja_template.template('bss_user/internet/bss_user_internet_youtube.html')
@common_global.auth.login_required
async def url_bp_user_internet_youtube(request):
    """
    Display youtube page
    """
    youtube_videos = []
    if request.ctx.session['search_text'] is not None:
        # TODO - ytpy search instead
        videos, channels, playlists = g.google_instance.com_google_youtube_search(
            request.ctx.session['search_text'])
        for url_link in videos:
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'searchurllink': url_link})
            youtube_videos.append(
                g.google_instance.com_google_youtube_info(url_link, 'snippet'))
    else:
        # get trending for specified country code
        for url_link in common_network_youtube.com_net_yt_trending(locale.getdefaultlocale()[0]):
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'urllink': url_link})
            youtube_videos.append(g.google_instance.com_google_youtube_info(url_link, 'snippet'))
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'temphold': youtube_videos})
    return {
        'media': youtube_videos
    }


@blueprint_user_internet_youtube.route('/user_internet/youtube_detail/<uuid>')
@common_global.jinja_template.template('bss_user/internet/bss_user_internet_youtube_detail.html')
@common_global.auth.login_required
async def url_bp_user_internet_youtube_detail(request, uuid):
    """
    Display youtube details page
    """
    return {
        'media': g.google_instance.com_google_youtube_info(uuid),
        'data_guid': uuid
    }
