from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_home_media = Blueprint('name_blueprint_user_home_media',
                                      url_prefix='/user')


@blueprint_user_home_media.route('/home_media', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_home_media.html')
@common_global.auth.login_required
async def url_bp_user_home_media_list(request):
    """
    Display home page for home media
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    # TODO wrong movie query
    db_connection = await request.app.db_pool.acquire()
    media_data = await request.app.db_functions.db_meta_movie_list(db_connection, offset, per_page,
                                                                   request['session'][
                                                                       'search_text'])
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data
    }


@blueprint_user_home_media.route('/home_media_detail/<guid>')
@common_global.jinja_template.template('user/user_home_media_detail.html')
@common_global.auth.login_required
async def url_bp_user_home_media_detail(request, guid):
    """
    Display home page for home media
    """
    return {}
