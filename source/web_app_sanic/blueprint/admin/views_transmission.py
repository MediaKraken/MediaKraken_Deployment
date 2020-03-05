

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


@blueprint.route("/transmission")
@login_required
@admin_required
async def url_bp_admin_transmission(request):
    """
    Display transmission page
    """
    trans_connection = common_transmission.CommonTransmission(
        g.option_config_json)
    transmission_data = []
    if trans_connection is not None:
        torrent_no = 1
        for torrent in trans_connection.com_trans_get_torrent_list():
            transmission_data.append(
                (common_internationalization.com_inter_number_format(torrent_no),
                 torrent.name, torrent.hashString, torrent.status,
                 torrent.progress, torrent.ratio))
            torrent_no += 1
    return render_template("admin/admin_transmission.html",
                           data_transmission=transmission_data)


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

