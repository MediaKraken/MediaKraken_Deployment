from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_media_new = Blueprint('name_blueprint_user_media_new', url_prefix='/user')


@blueprint_user_media_new.route('/user_media_new', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_new.html')
@common_global.auth.login_required
async def url_bp_user_media_new(request):
    """
    Display new media
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    request.ctx.session['search_page'] = 'new_media'
    media_data = []
    db_connection = await request.app.db_pool.acquire()
    for media_file in await request.app.db_functions.db_media_new(offset, int(request.ctx.session[
                                                                                  'per_page']),
                                                                  request.ctx.session[
                                                                      'search_text'],
                                                                  days_old=7,
                                                                  db_connection=db_connection):
        media_data.append(
            (media_file['mm_media_class_guid'],
             media_file['mm_media_name'], None))
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page=page,
                                                                      url='/user/user_media_new',
                                                                      item_count=await request.app.db_functions.db_meta_movie_count(
                                                                          request.ctx.session[
                                                                              'search_text'],
                                                                          days_old=7,
                                                                          db_connection=db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'pagination_links': pagination,
    }
