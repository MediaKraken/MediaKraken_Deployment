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
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_game_server',
                                                                      item_count=await request.app.db_functions.db_table_count(
                                                                          db_connection,
                                                                          'mm_game_dedicated_servers'),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    media_data = await request.app.db_functions.db_game_server_list(db_connection, offset,
                                                                    int(request.ctx.session[
                                                                            'per_page']))
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'pagination_links': pagination,
    }
