from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_media_new = Blueprint('name_blueprint_user_media_new', url_prefix='/user')


@blueprint_user_media_new.route('/media_new', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_media_new.html')
@common_global.auth.login_required
async def url_bp_user_media_new(request):
    """
    Display new media
    """
    page, per_page, offset = Pagination.get_page_args(request)
    request['session']['search_page'] = 'new_media'
    media_data = []
    for media_file in g.db_connection.db_read_media_new(offset, per_page,
                                                        request['session']['search_text'],
                                                        days_old=7):
        media_data.append(
            (media_file['mm_media_class_type'],
             media_file['mm_media_name'], None))
    pagination = Pagination(request,
                            total=g.db_connection.db_read_media_new_count(
                                request['session']['search_text'],
                                days_old=7),
                            record_name='new media',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
