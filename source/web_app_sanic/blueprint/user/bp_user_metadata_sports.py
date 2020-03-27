from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_sports = Blueprint('name_blueprint_user_metadata_sports',
                                           url_prefix='/user')


@blueprint_user_metadata_sports.route('/user_meta_sports_detail/<guid>')
@common_global.jinja_template.template('bss_user/meta_sports_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_sports_detail(request, guid):
    """
    Display sports detail metadata
    """
    db_connection = await request.app.db_pool.acquire()
    media_data = await request.app.db_functions.db_meta_sports_guid_by_thesportsdb(db_connection,
                                                                                   guid)
    await request.app.db_pool.release(db_connection)
    return {
        'guid': guid,
        'data': media_data
    }


@blueprint_user_metadata_sports.route('/user_meta_sports_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/meta_sports_list.html')
@common_global.auth.login_required
async def url_bp_user_metadata_sports_list(request):
    """
    Display sports metadata list
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_meta_sports_list(db_connection,
                                                                       offset, per_page,
                                                                       request['session'][
                                                                           'search_text']):
        media.append((row_data['mm_metadata_sports_guid'],
                      row_data['mm_metadata_sports_name']))
    request['session']['search_page'] = 'meta_sports'
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_meta_sports_list_count(
                                db_connection,
                                request['session']['search_text']),
                            record_name='sporting event(s)',
                            format_total=True,
                            format_number=True,
                            )
    media_data = await request.app.db_functions.db_meta_sports_list(db_connection, offset, per_page,
                                                                    request['session'][
                                                                        'search_text'])
    await request.app.db_pool.release(db_connection)
    return {
        'media_sports_list': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
