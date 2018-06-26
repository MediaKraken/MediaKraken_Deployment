"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from MediaKraken.user.forms import SyncEditForm
from quart import Blueprint, render_template, g, request, \
    redirect, url_for
from flask_login import login_required

blueprint = Blueprint("user_sync", __name__,
                      url_prefix='/users', static_folder="../static")
import json
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/sync')
@login_required
async def sync_display_all():
    """
    Display sync page
    """
    page, per_page, offset = common_pagination.get_page_items()
    # 0 - mm_sync_guid uuid, 1 - mm_sync_path, 2 - mm_sync_path_to, 3 - mm_sync_options_json
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_sync_list_count(),
                                                  record_name='Sync Jobs',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return await render_template('users/user_sync.html',
                           media_sync=g.db_connection.db_sync_list(
                               offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/sync_edit/<guid>', methods=['GET', 'POST'])
@login_required
async def sync_edit(guid):
    """
    Allow user to edit sync page
    """
    if request.method == 'POST':
        sync_json = {'Type': await request.form['target_type'],
                     'Media GUID': guid,
                     'Options': {'VContainer': await request.form['target_container'],
                                 'VCodec': await request.form['target_codec'],
                                 'Size': await request.form['target_file_size'],
                                 'AudioChannels': await request.form['target_audio_channels'],
                                 'ACodec': await request.form['target_audio_codec'],
                                 'ASRate': await request.form['target_sample_rate']},
                     'Priority': await request.form['target_priority'],
                     'Status': 'Scheduled',
                     'Progress': 0}
        g.db_connection.db_sync_insert(await request.form['name'],
                                       await request.form['target_output_path'], json.dumps(sync_json))
        g.db_connection.db_commit()
        return redirect(url_for('user.movie_detail', guid=guid))
    form = SyncEditForm(await request.form, csrf_enabled=False)
    if form.validate_on_submit():
        pass
    return await render_template('users/user_sync_edit.html', guid=guid, form=form)


@blueprint.route('/sync_delete', methods=["POST"])
@login_required
async def admin_sync_delete_page():
    """
    Display sync delete action 'page'
    """
    g.db_connection.db_sync_delete(await request.form['id'])
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
def teardown_request(exception):  # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
