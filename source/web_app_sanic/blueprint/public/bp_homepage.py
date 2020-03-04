from common import common_global
from sanic import Blueprint

blueprint_public_homepage = Blueprint('name_blueprint_public_homepage', url_prefix='/public')


@blueprint_public_homepage.route('/home', methods=['GET', 'POST'])
@common_global.jinja_template.template('public/home.html')
async def url_bp_homepage(request):
    """
    Display home page
    """
    return {}
