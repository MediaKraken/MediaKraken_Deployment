from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_game = Blueprint('name_blueprint_user_metadata_game', url_prefix='/user')


@blueprint_user_metadata_game.route('/meta_game', methods=["GET", "POST"])
@common_global.jinja_template.template('user/meta_game.html')
@common_global.auth.login_required
async def url_bp_user_metadata_game(request):
    """
    Display game list metadata
    """
    page, per_page, offset = Pagination.get_page_args(request)
    request['session']['search_page'] = 'meta_game'
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_table_count(db_connection,
                                'mm_metadata_game_software_info'),
                            record_name='game(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media_game': await request.app.db_functions.db_meta_game_list(db_connection, offset, per_page,
                                                        request['session']['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_metadata_game.route('/meta_game_detail/<guid>')
@common_global.jinja_template.template('user/meta_game_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_game_detail(request, guid):
    """
    Display game metadata detail
    """
    return {
        'guid': guid,
        'data': await request.app.db_functions.db_meta_game_by_guid(db_connection,
            guid)['gi_game_info_json'],
        'data_review': None,
    }
