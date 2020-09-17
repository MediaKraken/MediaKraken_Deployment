import json

from common import common_global
from sanic import Blueprint

blueprint_admin_hardware_tvtuner = Blueprint('name_blueprint_admin_hardware_tvtuner',
                                             url_prefix='/admin')


@blueprint_admin_hardware_tvtuner.route('/admin_tvtuner_by_id', methods=['POST'])
@common_global.auth.login_required
async def url_bp_admin_gettvtunerbyid(request):
    db_connection = await request.app.db_pool.acquire()
    result = await request.app.db_functions.db_device_by_uuid(request.form['id'],
                                                              db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return json.dumps({'Id': result['mm_device_id'],
                       'Name': result['mm_device_json']['Name'],
                       'IP': result['mm_device_json']['IP']})


@blueprint_admin_hardware_tvtuner.route('/admin_tvtuner_update', methods=['POST'])
@common_global.auth.login_required
async def url_bp_admin_updatetvtuner(request):
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_device_update_by_uuid(request.form['name'],
                                                            request.form['ipaddr'],
                                                            request.form['id'],
                                                            db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})
