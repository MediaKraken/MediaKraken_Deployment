from common import common_global
from sanic import Blueprint

blueprint_user_internet = Blueprint('name_blueprint_user_internet', url_prefix='/user')


@blueprint_user_internet.route('/internet', methods=['GET'])
@common_global.jinja_template.template('user/user_internet.html')
@common_global.auth.login_required
async def url_bp_user_internet(request):
    """
    Display internet page
    """
    return {}


# vimeo
@blueprint_user_internet.route('/internet/vimeo')
@common_global.jinja_template.template('user/user_internet_vimeo.html')
@common_global.auth.login_required
async def url_bp_user_internet_vimeo(request):
    """
    Display vimeo page
    """
    return {}


# flickr
@blueprint_user_internet.route('/internet/flickr')
@common_global.jinja_template.template('user/user_internet_flickr.html')
@common_global.auth.login_required
async def url_bp_user_internet_flickr(request):
    """
    Display main page for flickr
    """
    return {}
