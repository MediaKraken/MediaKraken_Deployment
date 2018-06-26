# -*- coding: utf-8 -*-

import json
import sys

sys.path.append('..')
from quart import Blueprint, render_template, g, request, flash, \
    url_for, redirect
from flask_login import login_required

blueprint = Blueprint("admins_tvtuners", __name__, url_prefix='/admin',
                      static_folder="../static")
# need the following three items for admin check
import quart
from flask_login import current_user
from functools import wraps
from MediaKraken.admins.forms import TVTunerEditForm

from common import common_config_ini
from common import common_global
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


def flash_errors(form):
    """
    Display errors from list
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


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
            return quart.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route("/tvtuners", methods=["GET", "POST"])
@login_required
@admin_required
async def admin_tvtuners():
    """
    List tvtuners
    """
    tv_tuners = []
    for row_data in g.db_connection.db_device_list('tvtuner'):
        tv_tuners.append((row_data['mm_device_id'], row_data['mm_device_json']['HWModel']
                          + " (" + row_data['mm_device_json']['Model'] + ")",
                          row_data['mm_device_json']['IP'],
                          len(row_data['mm_device_json']['Channels']),
                          row_data['mm_device_json']['Firmware'],
                          row_data['mm_device_json']['Active']))
    return await render_template("admin/admin_tvtuners.html", data_tuners=tv_tuners)


@blueprint.route("/tvtuner_edit", methods=["GET", "POST"])
@login_required
@admin_required
async def admin_tvtuner_edit_page():
    """
    allow user to edit tuner
    """
    form = TVTunerEditForm(await request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if await request.form['action_type'] == 'Add':
                # verify it doesn't exit and add
                if g.db_connection.db_device_check(await request.form['name'],
                                                   await request.form['ipaddr']) == 0:
                    g.db_connection.db_device_insert('tvtuner',
                                                     json.dumps({'Name': await request.form['name'],
                                                                 'Model': "NA",
                                                                 'IP': await request.form['ipaddr']}))
                    g.db_connection.db_commit()
                    return redirect(url_for('admins_tvtuners.admin_tvtuners'))
                else:
                    flash("TV Tuner already in database.", 'error')
                    return redirect(url_for('admins_tvtuners.admin_tuner_edit_page'))
        else:
            flash_errors(form)
    return await render_template("admin/admin_tuner_edit.html", form=form)


@blueprint.route('/tvtuner_delete', methods=["POST"])
@login_required
@admin_required
async def admin_tvtuner_delete_page():
    """
    Delete action 'page'
    """
    g.db_connection.db_device_delete(await request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/getTVTunerById', methods=['POST'])
@login_required
@admin_required
async def getTVTunerById():
    result = g.db_connection.db_device_by_uuid(await request.form['id'])
    return json.dumps({'Id': result['mm_device_id'],
                       'Name': result['mm_device_json']['Name'],
                       'IP': result['mm_device_json']['IP']})


@blueprint.route('/updateTVTuner', methods=['POST'])
@login_required
@admin_required
async def updateTVTuner():
    g.db_connection.db_device_update_by_uuid(await request.form['name'],
                                             await request.form['ipaddr'], await request.form['id'])
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
