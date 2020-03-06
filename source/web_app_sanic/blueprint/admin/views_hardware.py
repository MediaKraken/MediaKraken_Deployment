@blueprint.route('/getChromecastById', methods=['POST'])
@login_required
@admin_required
async def url_bp_admin_getChromecastById(request):
    result = g.db_connection.db_device_by_uuid(request.form['id'])
    return json.dumps({'Id': result['mm_device_id'],
                       'Name': result['mm_device_json']['Name'],
                       'IP': result['mm_device_json']['IP']})


@blueprint.route('/updateChromecast', methods=['POST'])
@login_required
@admin_required
async def url_bp_admin_updateChromecast(request):
    g.db_connection.db_device_update_by_uuid(request.form['name'],
                                             request.form['ipaddr'], request.form['id'])
    return json.dumps({'status': 'OK'})


@blueprint.route('/gettvtunerbyid', methods=['POST'])
@login_required
@admin_required
async def url_bp_admin_gettvtunerbyid(request):
    result = g.db_connection.db_device_by_uuid(request.form['id'])
    return json.dumps({'Id': result['mm_device_id'],
                       'Name': result['mm_device_json']['Name'],
                       'IP': result['mm_device_json']['IP']})


@blueprint.route('/updatetvtuner', methods=['POST'])
@login_required
@admin_required
async def url_bp_admin_updatetvtuner(request):
    g.db_connection.db_device_update_by_uuid(request.form['name'],
                                             request.form['ipaddr'], request.form['id'])
    return json.dumps({'status': 'OK'})
