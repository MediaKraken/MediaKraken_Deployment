# -*- coding: utf-8 -*-

import json
import sys

sys.path.append('..')
from flask import Blueprint, render_template, g, request, redirect, url_for
from flask_login import login_required

blueprint = Blueprint("admins_cron", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from MediaKraken.admins.forms import CronEditForm
from common import common_config_ini
from common import common_global
from common import common_network_pika
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


def admin_required(fn):
    """
    Admin check
    """

    @wraps(fn)
    @login_required
    def decorated_view(*args, **kwargs):
        common_global.es_inst.com_elastic_index('info',
                                                {"admin access attempt by": current_user.get_id()})
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route('/cron')
@login_required
@admin_required
def admin_cron_display_all():
    """
    Display cron jobs
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_cron_list_count(False),
                                                  record_name='Cron Jobs',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('admin/admin_cron.html',
                           media_cron=g.db_connection.db_cron_list(False, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/cron_run/<guid>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_cron_run(guid):
    """
    Run cron jobs
    """
    common_global.es_inst.com_elastic_index('info', {'admin cron run': guid})
    cron_job_data = g.db_connection.db_cron_info(guid)
    # submit the message
    common_network_pika.com_net_pika_send({'Type': cron_job_data['mm_cron_json']['type'],
                                           'User': current_user.get_id(),
                                           'JSON': cron_job_data['mm_cron_json']},
                                          exchange_name=cron_job_data['mm_cron_json'][
                                              'exchange_key'],
                                          route_key=cron_job_data['mm_cron_json']['route_key'])
    g.db_connection.db_cron_time_update(cron_job_data['mm_cron_name'])
    return redirect(url_for('admins_cron.admin_cron_display_all'))


@blueprint.route('/cron_edit/<guid>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_cron_edit(guid):
    """
    Edit cron job page
    """
    form = CronEditForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():
            request.form['name']
            request.form['description']
            request.form['enabled']
            request.form['interval']
            request.form['time']
            request.form['json']
    return render_template('admin/admin_cron_edit.html', guid=guid, form=form)


@blueprint.route('/cron_delete', methods=["POST"])
@login_required
@admin_required
def admin_cron_delete_page():
    """
    Delete action 'page'
    """
    g.db_connection.db_cron_delete(request.form['id'])
    g.db_connection.db_commit()
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
