


def admin_required(fn):
    """
    Admin check
    """

    @wraps(fn)
    @login_required
    def decorated_view(*args, **kwargs):
        common_global.es_inst.com_elastic_index('info', {"admin access attempt by":
                                                             current_user.get_id()})
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route("/users")
@login_required
@admin_required
def admin_users():
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
    return render_template('admin/admin_users.html',
                           users=g.db_connection.db_user_list_name(
                               offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route("/user_detail/<guid>")
@login_required
@admin_required
def admin_user_detail(guid):
    """
    Display user details
    """
    return render_template('admin/admin_user_detail.html',
                           data_user=g.db_connection.db_user_detail(guid))


@blueprint.route('/user_delete', methods=["POST"])
@login_required
@admin_required
def admin_user_delete_page():
    """
    Delete user action 'page'
    """
    g.db_connection.db_user_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})
