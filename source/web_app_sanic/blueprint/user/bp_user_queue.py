from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_queue = Blueprint('name_blueprint_user_queue', url_prefix='/user')


@blueprint_user_queue.route("/queue", methods=['GET'])
@common_global.jinja_template.template('user/user_queue.html')
async def url_bp_user_queue_page(request):
    """
    Display queue page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    # TODO union read all four.....then if first "group"....add header in the html
    common_global.session['search_page'] = 'user_media_queue'
    pagination = Pagination(request,
                            total=g.db_connection.db_web_tvmedia_list_count(
                                None, None,
                                common_global.session['search_text']),
                            record_name='queue',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': g.db_connection.db_meta_queue_list(current_user.get_id(), offset,
                                                    per_page,
                                                    common_global.session['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
