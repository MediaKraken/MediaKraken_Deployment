from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_periodical = Blueprint('name_blueprint_user_periodical', url_prefix='/user')


@blueprint_user_periodical.route('/periodical', methods=['GET'])
@common_global.jinja_template.template('user/user_periodical.html')
async def url_bp_user_periodical_list(request):
    """
    Display periodical page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    common_global.session['search_page'] = 'media_periodicals'
    pagination = Pagination(request,
                            total=g.db_connection.db_media_book_list_count(
                                common_global.session['search_text']),
                            record_name='periodical(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': g.db_connection.db_media_book_list(offset, per_page,
                                                    common_global.session['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_periodical.route('/periodical_detail/<guid>', methods=['GET'])
@common_global.jinja_template.template('user/user_periodical_detail.html')
async def url_bp_user_periodical_detail(request, guid):
    """
    Display periodical detail page
    """
    return {}
