from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_music_video = Blueprint('name_blueprint_user_music_video', url_prefix='/user')


@blueprint_user_music_video.route('/music_video', methods=['GET'])
@common_global.jinja_template.template('user/user_music_video.html')
async def url_bp_user_music_video_list(request):
    """
    Display music video page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    common_global.session['search_page'] = 'media_music_video'
    pagination = Pagination(request,
                            total=g.db_connection.db_music_video_list_count(
                                common_global.session['search_text']),
                            record_name='music video(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media_person': g.db_connection.db_music_video_list(offset, per_page,
                                                            common_global.session['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_music_video.route('/music_video_detail/<guid>', methods=['GET'])
async def url_bp_user_music_video_detail(request, guid):
    """
    Display music video detail page
    """
    return {}
