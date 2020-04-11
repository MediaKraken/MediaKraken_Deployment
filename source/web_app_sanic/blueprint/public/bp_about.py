from common import common_global
from sanic import Blueprint

blueprint_public_about = Blueprint('name_blueprint_public_about', url_prefix='/public')


@blueprint_public_about.route('/about', methods=["GET"])
@common_global.jinja_template.template('public/about.html')
async def url_bp_public_about(request):
    return {}
