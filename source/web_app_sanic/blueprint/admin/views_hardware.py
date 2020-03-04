

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


@blueprint.route("/hardware", methods=["GET", "POST"])
@login_required
@admin_required
def admin_hardware():
    if request.method == 'POST':
        # submit the message
        common_network_pika.com_net_pika_send({'Type': 'Hardware Scan'},
                                              rabbit_host_name='mkstack_rabbitmq',
                                              exchange_name='mkque_hardware_ex',
                                              route_key='mkhardware')
        flash("Scheduled hardware scan.")
    chromecast_list = []
    for row_data in g.db_connection.db_device_list('Chromecast'):
        if row_data['mm_device_json']['Model'] == 'Eureka Dongle':
            device_model = 'Chromecast'
        else:
            device_model = row_data['mm_device_json']['Model']
        chromecast_list.append((row_data['mm_device_id'],
                                row_data['mm_device_json']['Name'],
                                device_model,
                                row_data['mm_device_json']['IP'],
                                True))
    tv_tuners = []
    for row_data in g.db_connection.db_device_list('tvtuner'):
        tv_tuners.append((row_data['mm_device_id'], row_data['mm_device_json']['HWModel']
                          + " (" + row_data['mm_device_json']['Model'] + ")",
                          row_data['mm_device_json']['IP'],
                          len(row_data['mm_device_json']['Channels']),
                          row_data['mm_device_json']['Firmware'],
                          row_data['mm_device_json']['Active']))
    return render_template("admin/admin_hardware.html", data_chromecast=chromecast_list,
                           data_tuners=tv_tuners)


@blueprint.route("/chromecast_edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_chromecast_edit_page():
    """
    allow user to edit chromecast
    """
    form = ChromecastEditForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['action_type'] == 'Add':
                # verify it doesn't exit and add
                if g.db_connection.db_device_check(request.form['name'],
                                                   request.form['ipaddr']) == 0:
                    g.db_connection.db_device_insert('cast',
                                                     json.dumps({'Name': request.form['name'],
                                                                 'Model': "NA",
                                                                 'IP': request.form['ipaddr']}))
                    g.db_connection.db_commit()
                    return redirect(url_for('admins_chromecasts.admin_chromecast'))
                else:
                    flash("Chromecast already in database.", 'error')
                    return redirect(url_for('admins_chromecasts.admin_chromecast_edit_page'))
        else:
            flash_errors(form)
    return render_template("admin/admin_chromecast_edit.html", form=form)


@blueprint.route('/chromecast_delete', methods=["POST"])
@login_required
@admin_required
def admin_chromecast_delete_page():
    """
    Delete action 'page'
    """
    g.db_connection.db_device_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/getChromecastById', methods=['POST'])
@login_required
@admin_required
def getChromecastById():
    result = g.db_connection.db_device_by_uuid(request.form['id'])
    return json.dumps({'Id': result['mm_device_id'],
                       'Name': result['mm_device_json']['Name'],
                       'IP': result['mm_device_json']['IP']})


@blueprint.route('/updateChromecast', methods=['POST'])
@login_required
@admin_required
def updateChromecast():
    g.db_connection.db_device_update_by_uuid(request.form['name'],
                                             request.form['ipaddr'], request.form['id'])
    return json.dumps({'status': 'OK'})


@blueprint.route("/tvtuner_edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_tvtuner_edit_page():
    """
    allow user to edit tuner
    """
    form = TVTunerEditForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['action_type'] == 'Add':
                # verify it doesn't exit and add
                if g.db_connection.db_device_check(request.form['name'],
                                                   request.form['ipaddr']) == 0:
                    g.db_connection.db_device_insert('tvtuner',
                                                     json.dumps({'Name': request.form['name'],
                                                                 'Model': "NA",
                                                                 'IP': request.form['ipaddr']}))
                    g.db_connection.db_commit()
                    return redirect(url_for('admins_tvtuners.admin_tvtuners'))
                else:
                    flash("TV Tuner already in database.", 'error')
                    return redirect(url_for('admins_tvtuners.admin_tuner_edit_page'))
        else:
            flash_errors(form)
    return render_template("admin/admin_tuner_edit.html", form=form)


@blueprint.route('/tvtuner_delete', methods=["POST"])
@login_required
@admin_required
def admin_tvtuner_delete_page():
    """
    Delete action 'page'
    """
    g.db_connection.db_device_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/getTVTunerById', methods=['POST'])
@login_required
@admin_required
def getTVTunerById():
    result = g.db_connection.db_device_by_uuid(request.form['id'])
    return json.dumps({'Id': result['mm_device_id'],
                       'Name': result['mm_device_json']['Name'],
                       'IP': result['mm_device_json']['IP']})


@blueprint.route('/updateTVTuner', methods=['POST'])
@login_required
@admin_required
def updateTVTuner():
    g.db_connection.db_device_update_by_uuid(request.form['name'],
                                             request.form['ipaddr'], request.form['id'])
    return json.dumps({'status': 'OK'})

