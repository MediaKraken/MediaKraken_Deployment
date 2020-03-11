from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_game_system = Blueprint('name_blueprint_user_metadata_game_system',
                                                url_prefix='/user')


@blueprint_user_metadata_game_system.route('/meta_game_system', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_game_system.html')
@common_global.auth.login_required
async def url_bp_user_metadata_game_system(request):
    """
    Display list of game system metadata
    """
    page, per_page, offset = Pagination.get_page_args(request)
    request['session']['search_page'] = 'meta_game_system'
    pagination = Pagination(request,
                            total=await database_base_async.db_meta_game_system_list_count(db_connection),
                            record_name='game system(s)',
                            format_total=True,
                            format_number=True
                            )
    return {
        'media': await database_base_async.db_meta_game_system_list(db_connection, offset, per_page,
                                                          request['session']['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_metadata_game_system.route('/meta_game_system_detail/<guid>')
@common_global.jinja_template.template('user/meta_game_system_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_game_system_detail(request, guid):
    """
    Display metadata game detail
    """
    return {
        'guid': guid,
        'data': await database_base_async.db_meta_game_system_by_guid(db_connection, guid),
    }
