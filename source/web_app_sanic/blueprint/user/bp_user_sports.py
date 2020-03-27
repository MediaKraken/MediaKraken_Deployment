from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_sports = Blueprint('name_blueprint_user_sports', url_prefix='/user')


# list of spoting events
@blueprint_user_sports.route("/user_sports", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/user_sports.html')
@common_global.auth.login_required
async def url_bp_user_sports(request):
    """
    Display sporting events page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_media_sports_list(db_connection,
                                                                        common_global.DLMediaType.Sports.value,
                                                                        offset, per_page,
                                                                        request['session'][
                                                                            'search_text']):
        media.append((row_data['mm_metadata_sports_guid'],
                      row_data['mm_metadata_sports_name']))
    request['session']['search_page'] = 'media_sports'
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_media_sports_list_count(
                                db_connection,
                                request['session']['search_text']),
                            record_name='sporting event(s)',
                            format_total=True,
                            format_number=True,
                            )
    await request.app.db_pool.release(db_connection)
    return {'media': media,
            'page': page,
            'per_page': per_page,
            'pagination': pagination,
            }


@blueprint_user_sports.route("/user_sports_detail/<guid>", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/user_sports_detail.html')
@common_global.auth.login_required
async def url_bp_user_sports_detail(request, guid):
    """
    Display sports detail page
    """
    # poster image
    db_connection = await request.app.db_pool.acquire()
    media_data = await request.app.db_functions.db_meta_thesportsdb_select_by_guid(db_connection, guid)
    try:
        if json_metadata['LocalImages']['Poster'] is not None:
            data_poster_image = json_metadata['LocalImages']['Poster']
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    await request.app.db_pool.release(db_connection)
    return {
        'data': media_data,
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
    }
