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
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request, user.per_page)
    request.ctx.session['search_page'] = 'new_media'
    media_data = []
    db_connection = await request.app.db_pool.acquire()
    for media_file in await request.app.db_functions.db_media_new(db_connection, offset, per_page,
                                                        request.ctx.session['search_text'],
                                                        days_old=7):
        media_data.append(
            (media_file['mm_media_class_guid'],
             media_file['mm_media_name'], None))
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_media_new_count(db_connection,
                                request.ctx.session['search_text'],
                                days_old=7),
                            record_name='new media',
                            format_total=True,
                            format_number=True,
                            )
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
