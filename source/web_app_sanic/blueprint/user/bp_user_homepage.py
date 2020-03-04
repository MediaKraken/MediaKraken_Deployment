from common import common_global
from sanic import Blueprint

blueprint_user_homepage = Blueprint('name_blueprint_user_homepage', url_prefix='/user')


@blueprint_user_homepage.route('/home', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_home.html')
async def url_bp_user_homepage(request):
    """
    Display user home page
    """
    return {}
