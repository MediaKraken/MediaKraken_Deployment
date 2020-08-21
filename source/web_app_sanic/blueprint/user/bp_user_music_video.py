from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_music_video = Blueprint('name_blueprint_user_music_video', url_prefix='/user')


@blueprint_user_music_video.route('/user_music_video', methods=['GET'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_music_video.html')
@common_global.auth.login_required
async def url_bp_user_music_video_list(request):
    """
    Display music video page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    request.ctx.session['search_page'] = 'media_music_video'
    db_connection = await request.app.db_pool.acquire()
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_music_video_list_count(
                                db_connection,
                                request.ctx.session['search_text']),
                            record_name='music video(s)',
                            format_total=True,
                            format_number=True,
                            )
    media_data = await request.app.db_functions.db_music_video_list(db_connection, offset, per_page,
                                                                    request.ctx.session[
                                                                        'search_text'])
    await request.app.db_pool.release(db_connection)
    return {
        'media_person': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_music_video.route('/user_music_video_detail/<guid>', methods=['GET'])
@common_global.auth.login_required
async def url_bp_user_music_video_detail(request, guid):
    """
    Display music video detail page
    """
    return {}
