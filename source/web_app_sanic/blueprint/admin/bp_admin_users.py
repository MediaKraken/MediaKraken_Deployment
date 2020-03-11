import json
import database_async as database_base_async
from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_admin_users = Blueprint('name_blueprint_admin_users', url_prefix='/admin')


@blueprint_admin_users.route('/user_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_user_delete(request):
    """
    Delete user action 'page'
    """
    await database_base_async.db_user_delete(db_connection, request.form['id'])
    return json.dumps({'status': 'OK'})


@blueprint_admin_users.route("/user_detail/<guid>")
@common_global.jinja_template.template('admin/admin_user_detail.html')
@common_global.auth.login_required
async def url_bp_admin_user_detail(request, guid):
    """
    Display user details
    """
    return {'data_user': await database_base_async.db_user_detail(db_connection, guid)}


@blueprint_admin_users.route("/users")
@common_global.jinja_template.template('admin/admin_users.html')
@common_global.auth.login_required
async def url_bp_admin_user(request):
    """
    Display user list
    """
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=await database_base_async.db_user_list_name_count(db_connection),
                            record_name='users',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'users': await database_base_async.db_user_list_name(db_connection, offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
