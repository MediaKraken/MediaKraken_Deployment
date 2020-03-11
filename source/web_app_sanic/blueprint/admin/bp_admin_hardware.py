import json

import database_async as database_base_async
from common import common_global
from common import common_network_pika
from sanic import Blueprint
from sanic.response import redirect
from web_app_sanic.blueprint.admin.forms import ChromecastEditForm, TVTunerEditForm

blueprint_admin_hardware = Blueprint('name_blueprint_admin_hardware', url_prefix='/admin')


@blueprint_admin_hardware.route("/hardware", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_hardware.html')
@common_global.auth.login_required
async def url_bp_admin_hardware(request):
    if request.method == 'POST':
        # submit the message
        common_network_pika.com_net_pika_send({'Type': 'Hardware Scan'},
                                              rabbit_host_name='mkstack_rabbitmq',
                                              exchange_name='mkque_hardware_ex',
                                              route_key='mkhardware')
        request['flash']("Scheduled hardware scan.", "success")
    chromecast_list = []
    async with request.app.db_pool.acquire() as db_connection:
        for row_data in await request.app.db_functions.db_device_list(db_connection, 'Chromecast'):
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
    async with request.app.db_pool.acquire() as db_connection:
        for row_data in await request.app.db_functions.db_device_list(db_connection, 'tvtuner'):
            tv_tuners.append((row_data['mm_device_id'], row_data['mm_device_json']['HWModel']
                              + " (" + row_data['mm_device_json']['Model'] + ")",
                              row_data['mm_device_json']['IP'],
                              len(row_data['mm_device_json']['Channels']),
                              row_data['mm_device_json']['Firmware'],
                              row_data['mm_device_json']['Active']))
    return {
        'data_chromecast': chromecast_list,
        'data_tuners': tv_tuners,
    }


@blueprint_admin_hardware.route('/hardware_chromecast_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_hardware_chromecast_delete(request):
    """
    Delete action 'page'
    """
    async with request.app.db_pool.acquire() as db_connection:
        await request.app.db_functions.db_device_delete(db_connection, request.form['id'])
    return json.dumps({'status': 'OK'})


@blueprint_admin_hardware.route("/hardware_chromecast_edit", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_hardware_chromecast_edit.html')
@common_global.auth.login_required
async def url_bp_admin_hardware_chromecast_edit(request):
    """
    allow user to edit chromecast
    """
    form = ChromecastEditForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['action_type'] == 'Add':
                # verify it doesn't exit and add
                async with request.app.db_pool.acquire() as db_connection:
                    if await request.app.db_functions.db_device_check(db_connection,
                                                                 request.form['name'],
                                                                 request.form['ipaddr']) == 0:
                        request.app.db_functions.db_device_upsert(db_connection, 'cast',
                                                             json.dumps(
                                                                 {'Name': request.form['name'],
                                                                  'Model': "NA",
                                                                  'IP': request.form['ipaddr']}))
                        return redirect(request.app.url_for('admins_chromecasts.admin_chromecast'))
                    else:
                        request['flash']("Chromecast already in database.", 'error')
                        return redirect(
                            request.app.url_for('admins_chromecasts.admin_chromecast_edit_page'))
        else:
            flash_errors(form)
    return {
        'form': form
    }


@blueprint_admin_hardware.route("/hardware_tvtuner_edit", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_hardware_tuner_edit.html')
@common_global.auth.login_required
async def url_bp_admin_hardware_tvtuner_edit(request):
    """
    allow user to edit tuner
    """
    form = TVTunerEditForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['action_type'] == 'Add':
                # verify it doesn't exit and add
                async with request.app.db_pool.acquire() as db_connection:
                    if await request.app.db_functions.db_device_check(db_connection,
                                                                 request.form['name'],
                                                                 request.form['ipaddr']) == 0:
                        request.app.db_functions.db_device_upsert(db_connection, 'tvtuner',
                                                             json.dumps(
                                                                 {'Name': request.form['name'],
                                                                  'Model': "NA",
                                                                  'IP': request.form['ipaddr']}))
                        return redirect(request.app.url_for('admins_tvtuners.admin_tvtuners'))
                    else:
                        request['flash']("TV Tuner already in database.", 'error')
                        return redirect(
                            request.app.url_for('admins_tvtuners.admin_tuner_edit_page'))
        else:
            flash_errors(form)
    return {
        'form': form
    }


@blueprint_admin_hardware.route('/hardware_tvtuner_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_hardware_tvtuner_delete(request):
    """
    Delete action 'page'
    """
    async with request.app.db_pool.acquire() as db_connection:
        await request.app.db_functions.db_device_delete(db_connection, request.form['id'])
    return json.dumps({'status': 'OK'})
