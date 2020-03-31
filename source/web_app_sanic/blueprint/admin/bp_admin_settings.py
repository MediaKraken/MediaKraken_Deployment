from common import common_global
from sanic import Blueprint

blueprint_admin_settings = Blueprint('name_blueprint_admin_settings', url_prefix='/admin')


@blueprint_admin_settings.route("/admin_settings", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_settings.html')
@common_global.auth.login_required
async def url_bp_admin_settings(request):
    return {}
