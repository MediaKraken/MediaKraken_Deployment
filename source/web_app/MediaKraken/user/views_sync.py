"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from MediaKraken.user.forms import SyncEditForm
from flask import Blueprint, render_template, g, request, \
    redirect, url_for
from flask_login import login_required

blueprint = Blueprint("user_sync", __name__,
                      url_prefix='/users', static_folder="../static")
import json
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_pagination_flask
import database as database_base
from MediaKraken.utils import flash_errors


@blueprint.route('/sync')
@login_required
def sync_display_all():
    """
    Display sync page
    """
    page, per_page, offset = common_pagination_flask.get_page_items()
    # 0 - mm_sync_guid uuid, 1 - mm_sync_path, 2 - mm_sync_path_to, 3 - mm_sync_options_json
    pagination = common_pagination_flask.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_sync_list_count(),
                                                  record_name='sync job(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_sync.html',
                           media_sync=g.db_connection.db_sync_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/sync_edit/<guid>', methods=['GET', 'POST'])
@login_required
def sync_edit(guid):
    """
    Allow user to edit sync page
    """
    if request.method == 'POST':
        sync_json = {'Type': request.form['target_type'],
                     'Media GUID': guid,
                     'Options': {'VContainer': request.form['target_container'],
                                 'VCodec': request.form['target_codec'],
                                 'Size': request.form['target_file_size'],
                                 'AudioChannels': request.form['target_audio_channels'],
                                 'ACodec': request.form['target_audio_codec'],
                                 'ASRate': request.form['target_sample_rate']},
                     'Priority': request.form['target_priority'],
                     'Status': 'Scheduled',
                     'Progress': 0}
        g.db_connection.db_sync_insert(request.form['name'],
                                       request.form['target_output_path'], json.dumps(sync_json))
        g.db_connection.db_commit()
        return redirect(url_for('user.movie_detail', guid=guid))
    form = SyncEditForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        pass
    else:
        flash_errors(form)
    return render_template('users/user_sync_edit.html', guid=guid, form=form)


@blueprint.route('/sync_delete', methods=["POST"])
@login_required
def admin_sync_delete_page():
    """
    Display sync delete action 'page'
    """
    g.db_connection.db_sync_delete(request.form['id'])
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
