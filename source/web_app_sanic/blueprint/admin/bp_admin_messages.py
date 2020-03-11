import json

from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_admin_messages = Blueprint('name_blueprint_admin_messages', url_prefix='/admin')


@blueprint_admin_messages.route("/messages", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_messages.html')
@common_global.auth.login_required
async def url_bp_admin_messages(request):
    """
    List all messages
    """
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=g.db_connection.db_table_count(db_connection,
                                'mm_messages'),
                            record_name='messages(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media_dir': g.db_connection.db_message_list(db_connection, offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_messages.route('/message_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_messages_delete(request):
    """
    Delete messages action 'page'
    """
    g.db_connection.db_message_delete(db_connection, request.form['id'])
    return json.dumps({'status': 'OK'})
