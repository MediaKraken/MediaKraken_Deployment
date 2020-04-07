import json

from common import common_global
from common import common_internationalization
from common import common_transmission
from sanic import Blueprint

blueprint_admin_transmission = Blueprint('name_blueprint_admin_transmission', url_prefix='/admin')


@blueprint_admin_transmission.route("/admin_transmission")
@common_global.jinja_template.template('bss_admin/bss_admin_transmission.html')
@common_global.auth.login_required
async def url_bp_admin_transmission(request):
    """
    Display transmission page
    """
    db_connection = await request.app.db_pool.acquire()
    trans_connection = common_transmission.CommonTransmission(
        await request.app.db_functions.db_opt_json_read(db_connection))
    await request.app.db_pool.release(db_connection)
    transmission_data = []
    if trans_connection is not None:
        torrent_no = 1
        for torrent in trans_connection.com_trans_get_torrent_list():
            transmission_data.append(
                (common_internationalization.com_inter_number_format(torrent_no),
                 torrent.name, torrent.hashString, torrent.status,
                 torrent.progress, torrent.ratio))
            torrent_no += 1
    return {
        'data_transmission': transmission_data
    }


@blueprint_admin_transmission.route('/admin_transmission_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_transmission_delete(request):
    """
    Delete torrent from transmission
    """
    # await request.app.db_functions.db_transmission_delete(db_connection, request.form['id'])
    return json.dumps({'status': 'OK'})


@blueprint_admin_transmission.route('/admin_transmission_edit', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_transmission_edit(request):
    """
    Edit a torrent from transmission
    """
    # await request.app.db_functions.db_transmission_delete(db_connection, request.form['id'])
    return json.dumps({'status': 'OK'})
