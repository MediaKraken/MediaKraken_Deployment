import json

from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_admin_messages = Blueprint('name_blueprint_admin_messages', url_prefix='/admin')


@blueprint_admin_messages.route("/messages", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_messages.html')
@admin_required
async def url_bp_admin_messages(request):
    """
    List all messages
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_messages'),
                                                  record_name='messages(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return {
        'media_dir': g.db_connection.db_message_list(
            offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_messages.route('/message_delete', methods=["POST"])
@admin_required
async def url_bp_admin_messages_delete(request):
    """
    Delete messages action 'page'
    """
    g.db_connection.db_message_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})
