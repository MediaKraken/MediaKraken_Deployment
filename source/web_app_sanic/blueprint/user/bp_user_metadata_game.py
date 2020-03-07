from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_user_metadata_game = Blueprint('name_blueprint_user_metadata_game', url_prefix='/user')


@blueprint_user_metadata_game.route('/meta_game', methods=["GET", "POST"])
@common_global.jinja_template.template('user/meta_game.html')
async def url_bp_user_metadata_game(request):
    """
    Display game list metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    common_global.session['search_page'] = 'meta_game'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_game_software_info'),
                                                  record_name='game(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return {
        'media_game': g.db_connection.db_meta_game_list(offset, per_page,
                                                        common_global.session['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_metadata_game.route('/meta_game_detail/<guid>')
@common_global.jinja_template.template('user/meta_game_detail.html')
async def url_bp_user_metadata_game_detail(request, guid):
    """
    Display game metadata detail
    """
    return {
        'guid': guid,
        'data': g.db_connection.db_meta_game_by_guid(
            guid)['gi_game_info_json'],
        'data_review': None,
    }
