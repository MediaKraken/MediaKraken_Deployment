"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from flask import Blueprint, render_template, g, request, session
from flask_login import login_required

blueprint = Blueprint("user_music_video", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/music_video_list', methods=['GET', 'POST'])
@blueprint.route('/music_video_list/', methods=['GET', 'POST'])
@blueprint.route('/music_video_list/<search_text>/', methods=['GET', 'POST'])
@login_required
def user_music_video_list():
    """
    Display music video page
    """
    page, per_page, offset = common_pagination.get_page_items()
    if request.method == 'POST':
        mediadata = g.db_connection.db_music_video_list(offset, per_page, search_text)
    else:
        mediadata = g.db_connection.db_music_video_list(offset, per_page)
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_music_video'),
                                                  record_name='music video',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_music_video_list.html',
                           media_person=mediadata,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


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
