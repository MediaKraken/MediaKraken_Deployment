import json

from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_admin_users = Blueprint('name_blueprint_admin_users', url_prefix='/admin')


@blueprint_admin_users.route('/admin_user_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_user_delete(request):
    """
    Delete user action 'page'
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_user_delete(db_connection, request.form['id'])
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})


@blueprint_admin_users.route("/admin_user_detail/<guid>")
@common_global.jinja_template.template('bss_admin/bss_admin_user_detail.html')
@common_global.auth.login_required
async def url_bp_admin_user_detail(request, guid):
    """
    Display user details
    """
    db_connection = await request.app.db_pool.acquire()
    data_user = await request.app.db_functions.db_user_detail(db_connection, guid)
    await request.app.db_pool.release(db_connection)
    return {'data_user': data_user}


@blueprint_admin_users.route("/admin_users")
@common_global.jinja_template.template('bss_admin/bss_admin_user.html')
@common_global.auth.login_required
async def url_bp_admin_user(request):
    """
    Display user list
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/admin/admin_users',
                                                                      item_count=await request.app.db_functions.db_user_count(
                                                                          db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    data_users = await request.app.db_functions.db_user_list_name(db_connection,
                                                                  offset,
                                                                  int(request.ctx.session[
                                                                          'per_page']))
    await request.app.db_pool.release(db_connection)
    return {
        'users': data_users,
        'pagination': pagination,
        'page': page,
        'per_page': int(request.ctx.session['per_page'])
    }
