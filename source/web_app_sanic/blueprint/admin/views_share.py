@blueprint.route('/getsharebyid', methods=['POST'])
@login_required
@admin_required
async def url_bp_admin_getsharebyid(request):
    result = g.db_connection.db_audit_share_by_uuid(db_connection, request.form['id'])
    return json.dumps({'Id': result['mm_share_dir_guid'],
                       'Path': result['mm_share_dir_path']})


@blueprint.route('/updateshare', methods=['POST'])
@login_required
@admin_required
async def url_bp_admin_updateshare(request):
    g.db_connection.db_audit_share_update_by_uuid(db_connection, request.form['new_share_type'],
                                                  request.form['new_share_user'],
                                                  request.form['new_share_password'],
                                                  request.form['new_share_server'],
                                                  request.form['new_share_path'],
                                                  request.form['id'])
    return json.dumps({'status': 'OK'})
