

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


@blueprint.route("/messages", methods=["GET", "POST"])
@login_required
@admin_required
async def url_bp_admin_messages(request):
    """
    List all messages
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_messages'),
                                                  record_name='messages(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("admin/admin_messages.html",
                           media_dir=g.db_connection.db_message_list(
                               offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/message_delete', methods=["POST"])
@login_required
@admin_required
async def url_bp_admin_messages_delete(request):
    """
    Delete messages action 'page'
    """
    g.db_connection.db_message_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})

