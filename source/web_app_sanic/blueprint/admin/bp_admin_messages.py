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
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/admin/admin_messages',
                                                                      item_count=await request.app.db_functions.db_table_count(
                                                                          db_connection,
                                                                          'mm_messages'),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    media_dir = await request.app.db_functions.db_message_list(db_connection, offset,
                                                               int(request.ctx.session[
                                                                       'per_page']))
    await request.app.db_pool.release(db_connection)
    return {
        'media_dir': media_dir,
        'pagination_links': pagination,
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
