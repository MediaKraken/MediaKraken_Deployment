

@blueprint.route('/transmission_delete', methods=["POST"])
@login_required
@admin_required
async def url_bp_admin_transmission_delete(request):
    """
    Delete torrent from transmission
    """
    # g.db_connection.db_Audit_Path_Delete(request.form['id'])
    # g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/transmission_edit', methods=["POST"])
@login_required
@admin_required
async def url_bp_admin_transmission_edit(request):
    """
    Edit a torrent from transmission
    """
    # g.db_connection.db_Audit_Path_Delete(request.form['id'])
    # g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.before_request
async def before_request(request):
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.option_config_json = g.db_connection.db_opt_status_read()[0]
    g.db_connection.db_open()

