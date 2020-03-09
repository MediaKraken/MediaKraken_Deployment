from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_music_video = Blueprint('name_blueprint_user_metadata_music_video',
                                                url_prefix='/user')


@blueprint_user_metadata_music_video.route('/meta_music_video', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_music_video_list.html')
@common_global.auth.login_required
async def url_bp_user_metadata_music_video(request):
    """
    Display metadata music video
    """
    page, per_page, offset = Pagination.get_page_args(request)
    request['session']['search_page'] = 'meta_music_video'
    pagination = Pagination(request,
                            total=g.db_connection.db_meta_music_video_count(
                                None, request['session']['search_text']),
                            record_name='music video(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': g.db_connection.db_meta_music_video_list(offset, per_page,
                                                          request['session']['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_metadata_music_video.route('/meta_music_video_detail/<guid>')
@common_global.jinja_template.template('user/meta_music_video_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_music_video_detail(request, guid):
    """
    Display metadata music video detail
    """
    return {
        'media': g.db_connection.db_meta_music_video_detail_uuid(guid)
    }