"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_metadata_game", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/meta_game_list', methods=["GET", "POST"])
@login_required
def metadata_game_list():
    """
    Display game list metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'meta_game'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_game_software_info'),
                                                  record_name='game(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    media_list = g.db_connection.db_meta_game_list(offset, per_page, session['search_text'])
    return render_template('users/metadata/meta_game_list.html',
                           media_game=media_list,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_game_detail/<guid>')
@login_required
def metadata_game_detail(guid):
    """
    Display metadata game detail
    """
    return render_template('users/metadata/meta_game_detail.html',
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
