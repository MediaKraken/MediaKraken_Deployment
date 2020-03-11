from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_music = Blueprint('name_blueprint_user_music', url_prefix='/user')


@blueprint_user_music.route("/album_detail/<guid>")
@common_global.jinja_template.template('user/user_music_album_detail.html')
@common_global.auth.login_required
async def url_bp_user_album_detail_page(request, guid):
    """
    Display album detail page
    """
    return {}


@blueprint_user_music.route("/album_list")
@common_global.jinja_template.template('user/user_music_album.html')
@common_global.auth.login_required
async def url_bp_user_album_list_page(request):
    """
    Display album page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    for row_data in g.db_connection.db_media_album_list(db_connection, offset, per_page,
                                                        request['session']['search_text']):
        if 'mm_metadata_album_json' in row_data:
            media.append((row_data['mm_metadata_album_guid'], row_data['mm_metadata_album_name'],
                          row_data['mm_metadata_album_json']))
        else:
            media.append((row_data['mm_metadata_album_guid'],
                          row_data['mm_metadata_album_name'], None))
    request['session']['search_page'] = 'music_album'
    pagination = Pagination(request,
                            total=g.db_connection.db_media_album_count(db_connection,
                                request['session']['search_page']),
                            record_name='music album(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {'media': media,
            'page': page,
            'per_page': per_page,
            'pagination': pagination,
            }
