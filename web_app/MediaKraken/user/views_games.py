"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
blueprint = Blueprint("user_games", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/games')
@blueprint.route('/games/')
@login_required
def user_games_list():
    """
    Display games page
    """
    return render_template("users/user_game_list.html")


@blueprint.route('/games_detail/<guid>/', methods=['GET', 'POST'])
@blueprint.route('/games_detail/<guid>', methods=['GET', 'POST'])
@login_required
def user_games_detail(guid):
    """
    Display game detail page
    """
    return render_template("users/user_game_detail.html")


@blueprint.route('/meta_game_list')
@blueprint.route('/meta_game_list/')
@login_required
def metadata_game_list():
    """
    Display game list metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(\
                                                      'mm_metadata_game_software_info'),
                                                  record_name='Games',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_game_list.html',
                           media_game=g.db_connection.db_meta_game_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_game_detail/<guid>/')
@blueprint.route('/meta_game_detail/<guid>')
@login_required
def metadata_game_detail(guid):
    """
    Display game metadata detail
    """
    return render_template('users/metadata/meta_game_detail.html', guid=guid,
                           data=g.db_connection.db_meta_game_by_guid(guid)['gi_game_info_json'],
                           data_review=None)


@blueprint.route('/meta_game_system_list')
@blueprint.route('/meta_game_system_list/')
@login_required
def metadata_game_system_list():
    """
    Display game system metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.\
                                                      db_meta_game_system_list_count(),
                                                  record_name='Game Systems',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_game_system_list.html',
                           media_game_system=g.db_connection.db_meta_game_system_list(\
                               offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_game_system_detail/<guid>/')
@blueprint.route('/meta_game_system_detail/<guid>')
@login_required
def metadata_game_system_detail(guid):
    """
    Display game system detail metadata
    """
    return render_template('users/metadata/meta_game_system_detail.html', guid=guid,
                           data=g.db_connection.db_meta_game_system_by_guid(guid))


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception): # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
