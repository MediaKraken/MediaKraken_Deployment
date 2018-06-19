# -*- coding: utf-8 -*-

import json
import sys

sys.path.append('..')
from flask import Blueprint, render_template, g, request, flash, \
    url_for, redirect
from flask_login import login_required

blueprint = Blueprint("admins_task", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from MediaKraken.extensions import (
    fpika,
)
from MediaKraken.admins.forms import TaskEditForm

from common import common_config_ini
from common import common_global
from common import common_pagination
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
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route('/task')
@blueprint.route('/task/')
@login_required
@admin_required
def admin_task_display_all():
    """
    Display task jobs
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_task_list_count(
                                                      False),
                                                  record_name='task Jobs',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('admin/admin_task.html',
                           media_task=g.db_connection.db_task_list(
                               False, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/task_run/<guid>', methods=['GET', 'POST'])
@blueprint.route('/task_run/<guid>/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_task_run(guid):
    """
    Run task jobs
    """
    common_global.es_inst.com_elastic_index('info', {'admin task guid': guid,
                                                     'info': g.db_connection.db_task_info(guid)})
    task_info = g.db_connection.db_task_info(guid)['mm_task_json']
    # submit the message
    ch = fpika.channel()
    ch.basic_publish(exchange=task_info['exchange_key'], routing_key=task_info['route_key'],
                     body=json.dumps(
                         {'Type': task_info['task'],
                          'User': current_user.get_id()}))
    fpika.return_channel(ch)
    return redirect(url_for('admins_task.admin_task_display_all'))


@blueprint.route('/task_edit/<guid>/', methods=['GET', 'POST'])
@blueprint.route('/task_edit/<guid>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_task_edit(guid):
    """
    Edit task job page
    """
    form = TaskEditForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():
            # request.form['name']
            # request.form['description']
            # request.form['enabled']
            # request.form['interval']
            # request.form['time']
            # request.form['script_path']
            # common_global.es_inst.com_elastic_index('info', {'stuff':'task edit info: %s %s %s', (addr, share, path))
            pass
    return render_template('admin/admin_task_edit.html', guid=guid, form=form)


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
