"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
from fractions import Fraction
blueprint = Blueprint("user_metadata_game_system", __name__, url_prefix='/users', static_folder="../static")
import logging # pylint: disable=W0611
import subprocess
import natsort
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_internationalization
from common import common_pagination
from common import common_string
import database as database_base
from MediaKraken.public.forms import SearchForm


option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/meta_game_system_detail/<guid>/')
@blueprint.route('/meta_game_system_detail/<guid>')
@login_required
def metadata_game_system_detail(guid):
    """
    Display metadata game detail
    """
    return render_template('users/metadata/meta_game_system_detail.html',
                          )


@blueprint.route('/meta_game_system_list', methods=['GET', 'POST'])
@blueprint.route('/meta_game_system_list/', methods=['GET', 'POST'])
@login_required
def metadata_game_system_list():
    """
    Display list of game system metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    form = SearchForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
        mediadata = g.db_connection.db_meta_game_system_list(offset, per_page, request.form['search_text'])
    else:
        mediadata = g.db_connection.db_meta_game_system_list(offset, per_page)

    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_music'),
                                                  record_name='music',
                                                  format_total=True,
                                                  format_number=True,
                                                 )

    return render_template('users/metadata/meta_game_system_list.html', form=form,
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
def teardown_request(exception): # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
