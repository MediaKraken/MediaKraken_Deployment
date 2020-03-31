from common import common_global
from sanic import Blueprint

blueprint_user_media_3d = Blueprint('name_blueprint_user_media_3d', url_prefix='/user')


@blueprint_user_media_3d.route('/user_media_3d', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_3d.html')
@common_global.auth.login_required
async def url_bp_user_media_3d(request, guid):
    """
    Display 3
    """
    return {}
