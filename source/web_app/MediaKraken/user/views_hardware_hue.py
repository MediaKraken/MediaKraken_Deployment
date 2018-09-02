"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from MediaKraken.extensions import (
    fpika,
)
from flask import Blueprint, render_template, g
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user_hardware_hue", __name__, url_prefix='/users',
                      static_folder="../static")
import json
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/hardware_hue')
@login_required
def user_hardware_hue():
    """
    Display hardware page for hue
    """
    return render_template("users/user_hardware_hue.html")


@blueprint.route('/hardware_hue_on')
@login_required
def user_hardware_hue_on():
    """
    Hue on
    """
    ch = fpika.channel()
    ch.basic_publish(exchange='mkque_hardware_ex', routing_key='mkhardware',
                     body=json.dumps({'Type': 'Hardware', 'Subtype': 'Lights',
                                      'Hardware': 'Hue', 'Action': 'OnOff',
                                      'Setting': True, 'Target': '10.0.0.225',
                                      'LightList': (1,2,3)}))
    fpika.return_channel(ch)
    return render_template("users/user_hardware_hue.html")


@blueprint.route('/hardware_hue_off')
@login_required
def user_hardware_hue_off():
    """
    Hue off
    """
    ch = fpika.channel()
    ch.basic_publish(exchange='mkque_hardware_ex', routing_key='mkhardware',
                     body=json.dumps({'Type': 'Hardware', 'Subtype': 'Lights',
                                      'Hardware': 'Hue', 'Action': 'OnOff',
                                      'Setting': False, 'Target': '10.0.0.225',
                                      'LightList': (1,2,3)}))
    fpika.return_channel(ch)
    return render_template("users/user_hardware_hue.html")


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
