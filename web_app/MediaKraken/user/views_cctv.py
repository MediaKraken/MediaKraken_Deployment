"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
from MediaKraken.user.forms import SyncEditForm
blueprint = Blueprint("cctv", __name__, url_prefix='/users', static_folder="../static")
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


@blueprint.route('/cctv')
@blueprint.route('/cctv/')
@login_required
def cctv():
    """
    Display cctv page
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_sync_list_count(),
                                                  record_name='CCTV System(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/user_cctv.html',
                           media_sync=g.db_connection.db_sync_list(offset, per_page),
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
