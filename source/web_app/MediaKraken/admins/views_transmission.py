# -*- coding: utf-8 -*-

import json
import sys

sys.path.append('..')
from flask import Blueprint, render_template, g
from flask_login import login_required

blueprint = Blueprint("admins_transmission", __name__, url_prefix='/admin',
                      static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps

from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_transmission
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


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
def admin_transmission():
    """
    Display transmission page
    """
    trans_connection = common_transmission.CommonTransmission(
        option_config_json)
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
def admin_transmission_delete_page():
    """
    Delete torrent from transmission
    """
    # g.db_connection.db_Audit_Path_Delete(request.form['id'])
    # g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/transmission_edit', methods=["POST"])
@login_required
@admin_required
def admin_transmission_edit_page():
    """
    Edit a torrent from transmission
    """
    # g.db_connection.db_Audit_Path_Delete(request.form['id'])
    # g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception):
    """
    Executes after each request
    """
    g.db_connection.db_close()
