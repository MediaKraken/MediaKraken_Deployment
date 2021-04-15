from common import common_global
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
