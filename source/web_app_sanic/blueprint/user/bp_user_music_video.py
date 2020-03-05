from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_user_music_video = Blueprint('name_blueprint_user_music_video', url_prefix='/user')


@blueprint_user_music_video.route('/music_video', methods=['GET'])
@common_global.jinja_template.template('user/user_music_video.html')
async def url_bp_user_music_video_list(request):
    """
    Display music video page
    """
    page, per_page, offset = common_pagination.get_page_items()
    common_global.session['search_page'] = 'media_music_video'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
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
