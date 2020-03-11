from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_cctv = Blueprint('name_blueprint_user_cctv', url_prefix='/user')


@blueprint_user_cctv.route('/cctv')
@common_global.jinja_template.template('user/user_cctv.html')
@common_global.auth.login_required
async def url_bp_user_cctv(request):
    """
    Display cctv page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=g.db_connection.db_sync_list_count(db_connection),
                            record_name='CCTV System(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {'media_sync': g.db_connection.db_sync_list(db_connection, offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_cctv.route('/cctv_detail/<guid>')
@common_global.jinja_template.template('user/user_cctv_detail.html')
@common_global.auth.login_required
async def url_bp_user_cctv_detail(request, guid):
    """
    Display cctv detail
    """
    return {}
