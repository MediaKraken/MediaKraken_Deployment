# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
#import locale
#locale.setlocale(locale.LC_ALL, '')
import uuid
import pygal
import json
import logging # pylint: disable=W0611
import os
import sys
sys.path.append('..')
from flask import Blueprint, render_template, g, request, current_app, jsonify, flash,\
     url_for, redirect, session, abort
from flask_login import login_required
from flask_paginate import Pagination
blueprint = Blueprint("admins_cron", __name__, url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from functools import partial
from MediaKraken.extensions import (
    fpika,
)
from MediaKraken.admins.forms import CronEditForm

from common import common_config_ini
from common import common_internationalization
from common import common_pagination
from common import common_version
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
        logging.info("admin access attempt by %s" % current_user.get_id())
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)
    return decorated_view


@blueprint.route('/cron')
@blueprint.route('/cron/')
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
@blueprint.route('/cron_run/<guid>/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_cron_run(guid):
    """
    Run cron jobs
    """
    logging.info('admin cron run %s', guid)
    cron_file_path = g.db_connection.db_cron_info(guid)['mm_cron_file_path']
    route_key = 'mkque_metadata'
    if cron_file_path == './subprogram_postgresql_backup.py':
        route_key = 'mkque'
    elif cron_file_path == './subprogram_update_create_collections.py':
        route_key = 'mkque_metadata'
    elif cron_file_path == './subprogram_create_chapter_images.py':
        route_key = 'mkque'
    elif cron_file_path == './subprogram_postgresql_vacuum.py':
        route_key = 'mkque'
    elif cron_file_path == './subprogram_file_scan.py':
        route_key = 'mkque'
    elif cron_file_path == './subprogram_roku_thumbnail_generate.py':
        route_key = 'mkque'
    elif cron_file_path == './subprogram_schedules_direct_updates.py':
        route_key = 'mkque_metadata'
    elif cron_file_path == './subprogram_subtitle_downloader.py':
        route_key = 'mkque_metadata'
    elif cron_file_path == './subprogram_sync.py':
        route_key = 'mkque'
    elif cron_file_path == './subprogram_tvmaze_updates.py':
        route_key = 'mkque_metadata'
    elif cron_file_path == './subprogram_tmdb_updates.py':
        route_key = 'mkque_metadata'
    elif cron_file_path == './subprogram_thetvdb_updates.py':
        route_key = 'mkque_metadata'
    elif cron_file_path == './subprogram_metadata_trailer_download.py':
        route_key = 'mkque'
    # submit the message
    ch = fpika.channel()
    ch.basic_publish(exchange='mkque_ex', routing_key=route_key,
                     body=json.dumps(
                         {'Type': 'Cron Run',
                          'Data': cron_file_path,
                          'User': current_user.get_id()}))
    fpika.return_channel(ch)
    return render_template('admin/admin_cron.html')


@blueprint.route('/cron_edit/<guid>/', methods=['GET', 'POST'])
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
            # request.form['name']
            # request.form['description']
            # request.form['enabled']
            # request.form['interval']
            # request.form['time']
            # request.form['script_path']
            # logging.info('cron edit info: %s %s %s', (addr, share, path))
            pass
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
