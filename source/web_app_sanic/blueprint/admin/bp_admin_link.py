import json

from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint
from web_app_sanic.blueprint.admin.bss_form_link import BSSLinkAddEditForm

blueprint_admin_link = Blueprint('name_blueprint_admin_link', url_prefix='/admin')


@blueprint_admin_link.route("/admin_link")
@common_global.jinja_template.template('bss_admin/bss_admin_link.html')
@common_global.auth.login_required
async def url_bp_admin_server_link(request):
    """
    Display page for linking server
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/admin/admin_link',
                                                                      item_count=await request.app.db_functions.db_link_list_count(
                                                                          search_value=None,
                                                                          db_connection=db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    link_data = await request.app.db_functions.db_link_list(offset,
                                                            int(request.ctx.session['per_page']),
                                                            search_value=None,
                                                            db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'data': link_data,
        'pagination_links': pagination
    }


@blueprint_admin_link.route("/admin_link_edit", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_link_edit.html')
@common_global.auth.login_required
async def url_bp_admin_link_edit(request):
    """
    allow user to edit link
    """
    form = BSSLinkAddEditForm(request)
    return {
        'form': form,
        'data_class': None,
        'data_share': None,
    }


@blueprint_admin_link.route('/admin_link_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_link_delete(request):
    """
    Delete linked server action 'page'
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_link_delete(request.form['id'], db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})
