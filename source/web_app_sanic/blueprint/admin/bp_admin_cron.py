import json

from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_admin_cron = Blueprint('name_blueprint_admin_cron', url_prefix='/admin')


@blueprint_admin_cron.route('/cron')
@common_global.jinja_template.template('admin/admin_cron.html')
@admin_required
async def url_bp_admin_cron(request):
    """
    Display cron jobs
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_cron_list_count(False),
                                                  record_name='Cron Jobs',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return {
        'media_cron': g.db_connection.db_cron_list(False, offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_cron.route('/cron_delete', methods=["POST"])
@admin_required
async def url_bp_admin_cron_delete(request):
    """
    Delete action 'page'
    """
    g.db_connection.db_cron_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})
