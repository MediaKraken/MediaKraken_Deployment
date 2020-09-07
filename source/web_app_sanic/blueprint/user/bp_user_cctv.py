from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_cctv = Blueprint('name_blueprint_user_cctv', url_prefix='/user')


@blueprint_user_cctv.route('/user_cctv')
@common_global.jinja_template.template('bss_user/media/bss_user_media_cctv.html')
@common_global.auth.login_required
async def url_bp_user_cctv(request):
    """
    Display cctv page
    """
    db_connection = await request.app.db_pool.acquire()
    media_data = await request.app.db_functions.db_sync_list(db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'media_sync': media_data,
    }


@blueprint_user_cctv.route('/user_cctv_detail/<guid>')
@common_global.jinja_template.template('bss_user/media/bss_user_media_cctv_detail.html')
@common_global.auth.login_required
async def url_bp_user_cctv_detail(request, guid):
    """
    Display cctv detail
    """
    return {}
