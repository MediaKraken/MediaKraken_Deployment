from common import common_global
from sanic import Blueprint

blueprint_error = Blueprint('name_blueprint_error', url_prefix='/error')


@blueprint_error.route('/error', methods=["GET"])
@common_global.jinja_template.template('error/error.html')
async def url_bp_public_error(request):
    return {}
