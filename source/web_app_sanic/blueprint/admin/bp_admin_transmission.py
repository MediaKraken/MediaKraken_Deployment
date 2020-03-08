import json

from common import common_global
from common import common_internationalization
from common import common_transmission
from sanic import Blueprint

blueprint_admin_transmission = Blueprint('name_blueprint_admin_transmission', url_prefix='/admin')


@blueprint_admin_transmission.route("/transmission")
@common_global.jinja_template.template('admin/admin_transmission.html')
@common_global.auth.login_required
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
    return {
        'data_transmission': transmission_data
    }


@blueprint_admin_transmission.route('/transmission_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_transmission_delete(request):
    """
    Delete torrent from transmission
    """
    # g.db_connection.db_Audit_Path_Delete(request.form['id'])
    # g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint_admin_transmission.route('/transmission_edit', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_transmission_edit(request):
    """
    Edit a torrent from transmission
    """
    # g.db_connection.db_Audit_Path_Delete(request.form['id'])
    # g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})
