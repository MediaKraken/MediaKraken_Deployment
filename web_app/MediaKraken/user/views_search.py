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
blueprint = Blueprint("user_search", __name__, url_prefix='/users', static_folder="../static")
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


option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route("/search")
@blueprint.route("/search/")
@login_required
def search_media(genre):
    """
    Display search page
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []

    total = g.db_connection.db_web_media_list_count(
        g.db_connection.db_media_uuid_by_class('Movie'), list_type='movie', list_genre=genre,
        group_collection=False, include_remote=True)
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=total,
                                                  record_name='results',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/user_search.html', media=media,
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
