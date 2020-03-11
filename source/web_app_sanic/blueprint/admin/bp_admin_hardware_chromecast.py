import json

import database_async as database_base_async
from common import common_global
from sanic import Blueprint

blueprint_admin_hardware_chromecast = Blueprint('name_blueprint_admin_hardware_chromecast', url_prefix='/admin')

@blueprint_admin_hardware_chromecast.route('/chromecast_update', methods=['POST'])
@common_global.auth.login_required
async def url_bp_admin_chromecast_update(request):
    async with request.app.db_pool.acquire() as db_connection:
        await request.app.db_functions.db_device_update_by_uuid(db_connection, request.form['name'],
                                             request.form['ipaddr'], request.form['id'])
    return json.dumps({'status': 'OK'})


@blueprint_admin_hardware_chromecast.route('/chromecast_by_id', methods=['POST'])
@common_global.auth.login_required
async def url_bp_admin_getChromecastById(request):
    async with request.app.db_pool.acquire() as db_connection:
        result = await request.app.db_functions.db_device_by_uuid(db_connection, request.form['id'])
    return json.dumps({'Id': result['mm_device_id'],
                       'Name': result['mm_device_json']['Name'],
                       'IP': result['mm_device_json']['IP']})
