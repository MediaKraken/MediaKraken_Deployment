# -*- coding: utf-8 -*-

import json
import sys

sys.path.append('..')
from quart import Blueprint, render_template, g, request, flash
from flask_login import login_required

blueprint = Blueprint("admins_cron", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import quart
from flask_login import current_user
from functools import wraps
from MediaKraken.extensions import (
    fpika,
)
from MediaKraken.admins.forms import CronEditForm

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
            return quart.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route('/cron')
@blueprint.route('/cron/')
@login_required
@admin_required
async def admin_cron_display_all():
    """
    Display cron jobs
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_cron_list_count(
                                                      False),
                                                  record_name='Cron Jobs',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return await render_template('admin/admin_cron.html',
                           media_cron=g.db_connection.db_cron_list(
                               False, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/cron_run/<guid>', methods=['GET', 'POST'])
@blueprint.route('/cron_run/<guid>/', methods=['GET', 'POST'])
@login_required
@admin_required
async def admin_cron_run(guid):
    """
    Run cron jobs
    """
    common_global.es_inst.com_elastic_index('info', {'admin cron run': guid})
    cron_file_path = g.db_connection.db_cron_info(guid)['mm_cron_file_path']
    route_key = 'mkque'
    exchange_key = 'mkque_ex'
    # no need to do the check since default
    # if cron_file_path == './subprogram_postgresql_backup.py'\
    #     or cron_file_path == './subprogram_create_chapter_images.py':
    #     elif cron_file_path == './subprogram_postgresql_vacuum.py':
    #     elif cron_file_path == './subprogram_file_scan.py':
    #     elif cron_file_path == './subprogram_roku_thumbnail_generate.py':
    #     elif cron_file_path == './subprogram_sync.py':
    #     pass

    if cron_file_path == './subprogram_update_create_collections.py' \
            or cron_file_path == './subprogram_tmdb_updates.py':
        route_key = 'themoviedb'
        exchange_key = 'mkque_metadata_ex'

    if cron_file_path == './subprogram_schedules_direct_updates.py':
        # TODO
        route_key = 'mkque_metadata'
        exchange_key = 'mkque_metadata_ex'

    if cron_file_path == './subprogram_subtitle_downloader.py':
        # TODO
        route_key = 'mkque_metadata'
        exchange_key = 'mkque_metadata_ex'

    if cron_file_path == './subprogram_tvmaze_updates.py':
        route_key = 'tvmaze'
        exchange_key = 'mkque_metadata_ex'

    if cron_file_path == './subprogram_thetvdb_updates.py':
        route_key = 'thetvdb'
        exchange_key = 'mkque_metadata_ex'

    if cron_file_path == './subprogram_metadata_trailer_download.py':
        # TODO
        route_key = 'mkque_metadata'
        exchange_key = 'mkque_metadata_ex'
    # submit the message
    ch = fpika.channel()
    ch.basic_publish(exchange=exchange_key, routing_key=route_key,
                     body=json.dumps(
                         {'Type': 'Cron Run',
                          'Data': cron_file_path,
                          'User': current_user.get_id()}))
    fpika.return_channel(ch)
    return await render_template('admin/admin_cron.html')


@blueprint.route('/cron_edit/<guid>/', methods=['GET', 'POST'])
@blueprint.route('/cron_edit/<guid>', methods=['GET', 'POST'])
@login_required
@admin_required
async def admin_cron_edit(guid):
    """
    Edit cron job page
    """
    form = CronEditForm(await request.form, csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():
            # await request.form['name']
            # await request.form['description']
            # await request.form['enabled']
            # await request.form['interval']
            # await request.form['time']
            # await request.form['script_path']
            # common_global.es_inst.com_elastic_index('info', {'stuff':'cron edit info: %s %s %s', (addr, share, path))
            pass
    return await render_template('admin/admin_cron_edit.html', guid=guid, form=form)


@blueprint.route('/cron_delete', methods=["POST"])
@login_required
@admin_required
async def admin_cron_delete_page():
    """
    Delete action 'page'
    """
    g.db_connection.db_cron_delete(await request.form['id'])
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
