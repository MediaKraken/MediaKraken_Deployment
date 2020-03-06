import json

from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_admin_users = Blueprint('name_blueprint_admin_users', url_prefix='/admin')


@blueprint_admin_users.route('/user_delete', methods=["POST"])
@login_required
@admin_required
async def url_bp_admin_user_delete(request):
    """
    Delete user action 'page'
    """
    g.db_connection.db_user_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint_admin_users.route("/user_detail/<guid>")
@common_global.jinja_template.template('admin/admin_user_detail.html')
@admin_required
async def url_bp_admin_user_detail(request, guid):
    """
    Display user details
    """
    return {'data_user': g.db_connection.db_user_detail(guid)}


@blueprint_admin_users.route("/users")
@common_global.jinja_template.template('admin/admin_users.html')
@admin_required
async def url_bp_admin_user(request):
    """
    Display user list
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_user_list_name_count(),
                                                  record_name='users',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return {
        'users': g.db_connection.db_user_list_name(offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
