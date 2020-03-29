from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_media_iradio = Blueprint('name_blueprint_user_media_iradio', url_prefix='/user')


@blueprint_user_media_iradio.route('/user_iradio', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media_bss_user_media_iradio.html')
@common_global.auth.login_required
async def url_bp_user_iradio_list(request):
    """
    Display main page for internet radio
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    if request['session']['search_text'] is not None:
        mediadata = await request.app.db_functions.db_iradio_list(db_connection, offset, per_page,
                                                                  search_value=request['session'][
                                                                      'search_text'])
    else:
        mediadata = await request.app.db_functions.db_iradio_list(db_connection, offset, per_page)
    await request.app.db_pool.release(db_connection)
    return {}


@blueprint_user_media_iradio.route('/user_iradio_detail/<guid>')
@common_global.jinja_template.template('bss_user/media_bss_user_media_iradio.html')
@common_global.auth.login_required
async def url_bp_user_iradio_detail(request, guid):
    """
    Display main page for internet radio
    """
    pass
