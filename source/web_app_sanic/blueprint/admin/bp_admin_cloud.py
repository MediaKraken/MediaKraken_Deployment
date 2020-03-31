from common import common_global
from sanic import Blueprint

blueprint_admin_cloud = Blueprint('name_blueprint_admin_cloud', url_prefix='/admin')


@blueprint_admin_cloud.route("/admin_cloud", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_cloud.html')
@common_global.auth.login_required
async def url_bp_admin_cloud(request):
    return {}
