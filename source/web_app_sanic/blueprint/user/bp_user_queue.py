from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_queue = Blueprint('name_blueprint_user_queue', url_prefix='/user')


@blueprint_user_queue.route("/queue", methods=['GET'])
@common_global.jinja_template.template('user/user_queue.html')
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_queue_page(request, user):
    """
    Display queue page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    # TODO union read all four.....then if first "group"....add header in the html
    request['session']['search_page'] = 'user_media_queue'
    db_connection = await request.app.db_pool.acquire()
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_meta_queue_list_count(
                                db_connection,
                                None, None,
                                request['session']['search_text']),
                            record_name='queue',
                            format_total=True,
                            format_number=True,
                            )
    media_data = await request.app.db_functions.db_meta_queue_list(db_connection, user.id, offset,
                                                                   per_page,
                                                                   request['session'][
                                                                       'search_text'])
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
