from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_queue = Blueprint('name_blueprint_user_queue', url_prefix='/user')


@blueprint_user_queue.route("/user_queue", methods=['GET'])
@common_global.jinja_template.template('bss_user/user_queue.html')
@common_global.auth.login_required()
async def url_bp_user_queue(request):
    """
    Display queue page
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    # TODO union read all four.....then if first "group"....add header in the html
    request.ctx.session['search_page'] = 'user_media_queue'
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_queue',
                                                                      item_count=await request.app.db_functions.db_meta_queue_list_count(
                                                                          db_connection,
                                                                          common_global.auth.current_user(
                                                                              request)[0],
                                                                          request.ctx.session[
                                                                              'search_text']),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    media_data = await request.app.db_functions.db_meta_queue_list(db_connection,
                                                                   common_global.auth.current_user(
                                                                       request)[0],
                                                                   offset,
                                                                   int(request.ctx.session[
                                                                           'per_page']),
                                                                   request.ctx.session[
                                                                       'search_text'])
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'pagination_links': pagination,
    }
