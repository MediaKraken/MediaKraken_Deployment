from common import common_global
from sanic import Blueprint

blueprint_admin_emulation = Blueprint('name_blueprint_admin_emulation', url_prefix='/admin')


@blueprint_admin_emulation.route("/admin_emulation", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_emulation.html')
@common_global.auth.login_required
async def url_bp_emulation(request):
    """
    Game metadata stats and update screen
    """
    data_mame_version = None
    return {
        'data_mame_version': data_mame_version,
    }
