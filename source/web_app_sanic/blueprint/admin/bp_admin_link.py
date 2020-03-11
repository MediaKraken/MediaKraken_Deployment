import json
import database_async as database_base_async
from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint
from web_app_sanic.blueprint.admin.forms import LinkAddEditForm

blueprint_admin_link = Blueprint('name_blueprint_admin_link', url_prefix='/admin')


@blueprint_admin_link.route("/link")
@common_global.jinja_template.template('admin/admin_link.html')
@common_global.auth.login_required
async def url_bp_admin_server_link(request):
    """
    Display page for linking server
    """
    page, per_page, offset = Pagination.get_page_args(request)
    async with request.app.db_pool.acquire() as db_connection:
        pagination = Pagination(request,
                                total=await request.app.db_functions.db_link_list_count(db_connection),
                                record_name='linked servers',
                                format_total=True,
                                format_number=True,
                                )
        return {
            'data': await request.app.db_functions.db_link_list(db_connection, offset, per_page),
            'page': page,
            'per_page': per_page,
            'pagination': pagination
        }


@blueprint_admin_link.route("/link_edit", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_link_edit.html')
@common_global.auth.login_required
async def url_bp_admin_link_edit(request):
    """
    allow user to edit link
    """
    form = LinkAddEditForm(request.form)
    return {
        'form': form,
        'data_class': None,
        'data_share': None,
    }


@blueprint_admin_link.route('/link_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_link_delete(request):
    """
    Delete linked server action 'page'
    """
    async with request.app.db_pool.acquire() as db_connection:
        await request.app.db_functions.db_link_delete(db_connection, request.form['id'])
    return json.dumps({'status': 'OK'})
