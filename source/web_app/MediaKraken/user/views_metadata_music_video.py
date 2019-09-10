"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_metadata_music_video", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/meta_music_video_list', methods=['GET', 'POST'])
@login_required
def metadata_music_video_list():
    """
    Display metadata music video
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'meta_music_video'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_music_video_count(
                                                      None, session['search_text']),
                                                  record_name='music video(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_music_video_list.html',
                           media=g.db_connection.db_meta_music_video_list(offset, per_page,
                                                                          session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_music_video_detail/<guid>')
@login_required
def metadata_music_video_detail(guid):
    """
    Display metadata music video detail
    """
    return render_template('users/metadata/meta_music_video_detail.html',
                           media=g.db_connection.db_meta_music_video_detail_uuid(guid))


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
