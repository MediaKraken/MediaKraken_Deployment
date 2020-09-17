from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_periodical = Blueprint('name_blueprint_user_periodical', url_prefix='/user')


@blueprint_user_periodical.route('/user_periodical', methods=['GET'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_periodical.html')
@common_global.auth.login_required
async def url_bp_user_periodical_list(request):
    """
    Display periodical page
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    request.ctx.session['search_page'] = 'media_periodicals'
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_meta_game',
                                                                      item_count=await request.app.db_functions.db_media_book_list_count(
                                                                          request.ctx.session[
                                                                              'search_text'],
                                                                          db_connection=db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    media_data = await request.app.db_functions.db_media_book_list(offset,
                                                                   int(request.ctx.session[
                                                                           'per_page']),
                                                                   request.ctx.session[
                                                                       'search_text'],
                                                                   db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'pagination_links': pagination,
    }


@blueprint_user_periodical.route('/user_periodical_detail/<guid>', methods=['GET'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_periodical_detail.html')
@common_global.auth.login_required
async def url_bp_user_periodical_detail(request, guid):
    """
    Display periodical detail page
    """
    return {}
