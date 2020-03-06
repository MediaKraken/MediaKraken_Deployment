
@blueprint.route("/link_server")
@login_required
@admin_required
async def url_bp_admin_server_link(request):
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
async def url_bp_admin_link_edit(request):
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
async def url_bp_admin_link_delete(request):
    """
    Delete linked server action 'page'
    """
    g.db_connection.db_link_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})

