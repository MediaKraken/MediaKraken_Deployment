from common import common_global
from sanic import Blueprint

blueprint_error = Blueprint('name_blueprint_error', url_prefix='/error')


@blueprint_error.route('/error401', methods=["GET"])
@common_global.jinja_template.template('bss_error/bss_error_401.html')
async def url_bp_public_error_401(request):
    return {}


@blueprint_error.route('/error403', methods=["GET"])
@common_global.jinja_template.template('bss_error/bss_error_403.html')
async def url_bp_public_error_403(request):
    return {}


@blueprint_error.route('/error404', methods=["GET"])
@common_global.jinja_template.template('bss_error/bss_error_404.html')
async def url_bp_public_error_404(request):
    return {}


@blueprint_error.route('/error500', methods=["GET"])
@common_global.jinja_template.template('bss_error/bss_error_500.html')
async def url_bp_public_error_500(request):
    return {}
