from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_user_game = Blueprint('name_blueprint_user_game', url_prefix='/user')


@blueprint_user_game.route('/game', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_game.html')
async def url_bp_user_game(request):
    """
    Display game page
    """
    page, per_page, offset = common_pagination.get_page_items()
    common_global.session['search_page'] = 'media_games'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
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
