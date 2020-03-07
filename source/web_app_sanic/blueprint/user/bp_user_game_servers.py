from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_user_game_servers = Blueprint('name_blueprint_user_game_servers', url_prefix='/user')


@blueprint_user_game_servers.route('/game_server', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_game_server.html')
async def url_bp_user_game_server_list(request):
    """
    Display game server page
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_game_server_list_count(),
                                                  record_name='game servers(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return {
        'media': g.db_connection.db_game_server_list(offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
