from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_game_system = Blueprint('name_blueprint_user_metadata_game_system',
                                                url_prefix='/user')


@blueprint_user_metadata_game_system.route('/user_meta_game_system', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_game_system.html')
@common_global.auth.login_required
async def url_bp_user_metadata_game_system(request):
    """
    Display list of game system metadata
    """
    page, per_page, offset = Pagination.get_page_args(request)
    request['session']['search_page'] = 'meta_game_system'
    db_connection = await request.app.db_pool.acquire()
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_meta_game_system_list_count(
                                db_connection),
                            record_name='game system(s)',
                            format_total=True,
                            format_number=True
                            )
    media_data = await request.app.db_functions.db_meta_game_system_list(db_connection, offset,
                                                                         per_page,
                                                                         request['session'][
                                                                             'search_text'])
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_metadata_game_system.route('/user_meta_game_system_detail/<guid>')
@common_global.jinja_template.template(
    'bss_user/metadata/bss_user_metadata_game_system_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_game_system_detail(request, guid):
    """
    Display metadata game detail
    """
    db_connection = await request.app.db_pool.acquire()
    media_data = await request.app.db_functions.db_meta_game_system_by_guid(db_connection, guid)
    await request.app.db_pool.release(db_connection)
    return {
        'guid': guid,
        'data': media_data,
    }
