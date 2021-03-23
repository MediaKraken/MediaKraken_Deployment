from common import common_global
from sanic import Blueprint

blueprint_user_internet_flickr = Blueprint('name_blueprint_user_internet_flickr',
                                           url_prefix='/user')


@blueprint_user_internet_flickr.route('/user_internet/flickr')
@common_global.jinja_template.template('bss_user/internet/bss_user_internet_flickr.html')
@common_global.auth.login_required
async def url_bp_user_internet_flickr(request):
    """
    Display main page for flickr
    """
    return {}


@blueprint_user_internet_flickr.route(
    '/user_internet/internet/bss_user_internet_flickr_detail/<guid>')
@common_global.auth.login_required
async def url_bp_user_internet_flickr_detail(request, guid):
    """
    Display main page for flickr
    """
    return {}
