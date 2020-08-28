from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_metadata_music_video = Blueprint('name_blueprint_user_metadata_music_video',
                                                url_prefix='/user')


@blueprint_user_metadata_music_video.route('/user_meta_music_video', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_music_video.html')
@common_global.auth.login_required
async def url_bp_user_metadata_music_video(request):
    """
    Display metadata music video
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    request.ctx.session['search_page'] = 'meta_music_video'
    db_connection = await request.app.db_pool.acquire()
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_meta_music_video_count(
                                db_connection,
                                None, request.ctx.session['search_text']),
                            record_name='music video(s)',
                            format_total=True,
                            format_number=True,
                            )
    media_data = await request.app.db_functions.db_meta_music_video_list(db_connection, offset,
                                                                         per_page,
                                                                         request.ctx.session[
                                                                             'search_text'])
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_metadata_music_video.route('/user_meta_music_video_detail/<guid>')
@common_global.jinja_template.template(
    'bss_user/metadata/bss_user_metadata_music_video_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_music_video_detail(request, guid):
    """
    Display metadata music video detail
    """
    db_connection = await request.app.db_pool.acquire()
    media_data = await request.app.db_functions.db_meta_music_video_detail_uuid(db_connection, guid)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data
    }
