"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g
from flask_login import login_required
from flask_login import current_user

from MediaKraken.extensions import (
    fpika,
)

blueprint = Blueprint("user_chromecast", __name__, url_prefix='/users',
                      static_folder="../static")
import logging  # pylint: disable=W0611
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
    common_global.es_inst.com_elastic_index('info', {'stuff':'cast action: %s', action)
    common_global.es_inst.com_elastic_index('info', {'stuff':'case user: %s', current_user.get_id())
    if action == 'base':
        pass
    elif action == 'back':
        pass
    #    elif action == 'rewind':
    #        pass
    elif action == 'stop':
        ch = fpika.channel()
        ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
                         body=json.dumps({'Type': 'Stop', 'Sub': 'Cast',
                                          'User': current_user.get_id()}))
        fpika.return_channel(ch)
    elif action == 'play':
        ch = fpika.channel()
        ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
                         body=json.dumps({'Type': 'Play', 'Sub': 'Cast',
                                          'User': current_user.get_id(),
                                          'Data': g.db_connection.db_read_media(guid)[
                                              'mm_media_path'],
                                          'Target': '10.0.0.244'}))
        fpika.return_channel(ch)
    elif action == 'pause':
        ch = fpika.channel()
        ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
                         body=json.dumps({'Type': 'Pause', 'Sub': 'Cast',
                                          'User': current_user.get_id()}))
        fpika.return_channel(ch)
    #    elif action == 'ff':
    #        pass
    elif action == 'forward':
        pass
    elif action == 'mute':
        ch = fpika.channel()
        ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
                         body=json.dumps({'Type': 'Mute', 'Sub': 'Cast',
                                          'User': current_user.get_id()}))
        fpika.return_channel(ch)
    elif action == 'vol_up':
        ch = fpika.channel()
        ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
                         body=json.dumps({'Type': 'Volume Up', 'Sub': 'Cast',
                                          'User': current_user.get_id()}))
        fpika.return_channel(ch)
    elif action == 'vol down':
        ch = fpika.channel()
        ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
                         body=json.dumps({'Type': 'Volume Down', 'Sub': 'Cast',
                                          'User': current_user.get_id()}))
        fpika.return_channel(ch)
    return render_template("users/user_playback_cast.html", data_uuid=guid,
                           data_chromecast=db_connection.db_device_list('cast'))


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
