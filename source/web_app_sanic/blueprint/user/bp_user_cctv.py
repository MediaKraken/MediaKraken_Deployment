from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_user_cctv = Blueprint('name_blueprint_user_cctv', url_prefix='/user')


@blueprint_user_cctv.route('/cctv')
@common_global.jinja_template.template('user/user_cctv.html')
async def url_bp_user_cctv():
    """
    Display cctv page
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_sync_list_count(),
                                                  record_name='CCTV System(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return {'media_sync': g.db_connection.db_sync_list(
        offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_cctv.route('/cctv_detail/<guid>')
@common_global.jinja_template.template('user/user_cctv_detail.html')
async def url_bp_user_cctv_detail(guid):
    """
    Display cctv detail
    """
    return {}
