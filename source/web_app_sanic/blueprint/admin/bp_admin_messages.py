import json

from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_admin_messages = Blueprint('name_blueprint_admin_messages', url_prefix='/admin')


@blueprint_admin_messages.route("/admin_messages", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_messages.html')
@common_global.auth.login_required
async def url_bp_admin_messages(request):
    """
    List all messages
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request, user.per_page)
    db_connection = await request.app.db_pool.acquire()
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_table_count(db_connection,
                                                                                'mm_messages'),
                            record_name='messages(s)',
                            format_total=True,
                            format_number=True,
                            )
    media_dir = await request.app.db_functions.db_message_list(db_connection, offset, per_page)
    await request.app.db_pool.release(db_connection)
    return {
        'media_dir': media_dir,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_messages.route('/admin_message_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_messages_delete(request):
    """
    Delete messages action 'page'
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_message_delete(db_connection, request.form['id'])
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})
