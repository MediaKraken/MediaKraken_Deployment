

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


@blueprint.route("/link_server")
@login_required
@admin_required
def admin_server_link_server():
    """
    Display page for linking server
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_link_list_count(),
                                                  record_name='linked servers',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("admin/admin_link.html",
                           data=g.db_connection.db_link_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@blueprint.route("/link_edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_link_edit_page():
    """
    allow user to edit link
    """
    form = LinkAddEditForm(request.form)
    return render_template("admin/admin_link_edit.html", form=form,
                           data_class=None,
                           data_share=None)


@blueprint.route('/link_delete', methods=["POST"])
@login_required
@admin_required
def admin_link_delete_page():
    """
    Delete linked server action 'page'
    """
    g.db_connection.db_link_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})

