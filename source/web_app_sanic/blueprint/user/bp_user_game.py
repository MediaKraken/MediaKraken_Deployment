from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_game = Blueprint('name_blueprint_user_game', url_prefix='/user')


@blueprint_user_game.route('/game', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_game.html')
async def url_bp_user_game(request):
    """
    Display game page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    common_global.session['search_page'] = 'media_games'
    pagination = Pagination(request,
                            total=g.db_connection.db_meta_game_system_list_count(),
                            record_name='game system(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': g.db_connection.db_meta_game_system_list(offset, per_page,
                                                          common_global.session['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_game.route('/game_detail/<guid>', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_game_detail.html')
async def url_bp_user_game_detail(request, guid):
    """
    Display game detail page
    """
    return {}
