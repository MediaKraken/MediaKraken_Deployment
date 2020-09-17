from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_media_iradio = Blueprint('name_blueprint_user_media_iradio', url_prefix='/user')


@blueprint_user_media_iradio.route('/user_iradio', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_iradio.html')
@common_global.auth.login_required
async def url_bp_user_iradio_list(request):
    """
    Display main page for internet radio
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    if request.ctx.session['search_text'] is not None:
        mediadata = await request.app.db_functions.db_iradio_list(offset,
                                                                  int(request.ctx.session[
                                                                          'per_page']),
                                                                  search_value=request.ctx.session[
                                                                      'search_text'],
                                                                  db_connection=db_connection)
    else:
        mediadata = await request.app.db_functions.db_iradio_list(offset,
                                                                  int(request.ctx.session[
                                                                          'per_page']),
                                                                  db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {}


@blueprint_user_media_iradio.route('/user_iradio_detail/<guid>')
@common_global.jinja_template.template('bss_user/media/bss_user_media_iradio.html')
@common_global.auth.login_required
async def url_bp_user_iradio_detail(request, guid):
    """
    Display main page for internet radio
    """
    pass
