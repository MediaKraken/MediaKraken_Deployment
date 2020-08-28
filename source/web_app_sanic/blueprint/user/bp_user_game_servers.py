from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_game_servers = Blueprint('name_blueprint_user_game_servers', url_prefix='/user')


@blueprint_user_game_servers.route('/user_game_server', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_game_server.html')
@common_global.auth.login_required
async def url_bp_user_game_server_list(request):
    """
    Display game server page
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_table_count(
                                db_connection, 'mm_game_dedicated_servers'),
                            record_name='game servers(s)',
                            format_total=True,
                            format_number=True,
                            )
    media_data = await request.app.db_functions.db_game_server_list(db_connection, offset, per_page)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
