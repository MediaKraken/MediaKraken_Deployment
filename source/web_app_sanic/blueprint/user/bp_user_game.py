from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_game = Blueprint('name_blueprint_user_game', url_prefix='/user')


@blueprint_user_game.route('/user_game', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_game.html')
@common_global.auth.login_required
async def url_bp_user_game(request):
    """
    Display game page
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    request.ctx.session['search_page'] = 'media_games'
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_game',
                                                                      item_count=await request.app.db_functions.db_meta_game_system_list_count(
                                                                          db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    media_data = await request.app.db_functions.db_meta_game_system_list(db_connection, offset,
                                                                         int(request.ctx.session[
                                                                                 'per_page']),
                                                                         request.ctx.session[
                                                                             'search_text'])
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'pagination_links': pagination,
    }


@blueprint_user_game.route('/user_game_detail/<guid>', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_game_detail.html')
@common_global.auth.login_required
async def url_bp_user_game_detail(request, guid):
    """
    Display game detail page
    """
    return {}
