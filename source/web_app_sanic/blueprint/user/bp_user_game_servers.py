from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint
import database_async as database_base_async

blueprint_user_game_servers = Blueprint('name_blueprint_user_game_servers', url_prefix='/user')


@blueprint_user_game_servers.route('/game_server', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_game_server.html')
@common_global.auth.login_required
async def url_bp_user_game_server_list(request):
    """
    Display game server page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_game_server_list_count(db_connection),
                            record_name='game servers(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': await request.app.db_functions.db_game_server_list(db_connection, offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
