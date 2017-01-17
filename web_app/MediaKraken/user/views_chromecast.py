"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
blueprint = Blueprint("user_chromecast", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import json
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/cast/<action>/<guid>/')
@blueprint.route('/cast/<action>/<guid>')
@login_required
def user_cast(action, guid):
    """
    Display chromecast actions page
    """
    logging.info('cast action: %s', action)
    logging.info('case user: %s', current_user.get_id())
    if action == 'base':
        pass
    elif action == 'back':
        pass
#    elif action == 'rewind':
#        pass
    elif action == 'stop':
        current_app.com_celery_chrome_stop(json.dumps({'user': current_user.get_id()}))
    elif action == 'play':
        current_app.com_celery_chrome_play(json.dumps({'user': current_user.get_id(), \
            'path': g.db_connection.db_read_media(guid)['mm_media_path']}))
        #cast_proc = subprocess.Popen(['python', './stream2chromecast/stream2chromecast.py', \
        #'-devicename', '10.0.0.56', g.db_connection.db_read_media(guid)['mm_media_path']])
    elif action == 'pause':
        current_app.com_celery_chrome_stop(json.dumps({'user': current_user.get_id()}))
#    elif action == 'ff':
#        pass
    elif action == 'forward':
        pass
    elif action == 'mute':
        current_app.com_celery_chrome_stop(json.dumps({'user': current_user.get_id()}))
    elif action == 'vol_up':
        current_app.com_celery_chrome_stop(json.dumps({'user': current_user.get_id()}))
    elif action == 'vol down':
        current_app.com_celery_chrome_stop(json.dumps({'user': current_user.get_id()}))
    return render_template("users/user_playback_cast.html")


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
