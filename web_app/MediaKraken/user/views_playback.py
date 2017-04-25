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
blueprint = Blueprint("user_playback", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/playback/<vid_type>/<guid>/')
@blueprint.route('/playback/<vid_type>/<guid>')
@login_required
def user_playback(vid_type, guid):
    """
    Display playback actions page
    """
    logging.info('playback action: %s', vid_type)
    logging.info('playback user: %s', current_user.get_id())
    return render_template("users/user_playback_videojs.html",
                           data_mtype=vid_type,
                           data_uuid=guid)


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
