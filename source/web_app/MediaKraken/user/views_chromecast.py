"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user_chromecast", __name__, url_prefix='/users',
                      static_folder="../static")
import json
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_network_pika
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/cast/<action>/<guid>')
@login_required
def user_cast(action, guid):
    """
    Display chromecast actions page
    """
    common_global.es_inst.com_elastic_index('info', {'cast action': action,
                                                     'case user': current_user.get_id()})
    if action == 'base':
        pass
    elif action == 'back':
        pass
    #    elif action == 'rewind':
    #        pass
    elif action == 'stop':
        common_network_pika.com_net_pika_send({'Type': 'Stop', 'Subtype': 'Cast',
                                               'User': current_user.get_id()},
                                              rabbit_host_name='mkrabbitmq',
                                              exchange_name='mkque_ex',
                                              route_key='mkque')
        # ch = fpika.channel()
        # ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
        #                  body=json.dumps({'Type': 'Stop', 'Subtype': 'Cast',
        #                                   'User': current_user.get_id()}),
        #                  properties=fpika.BasicProperties(content_type='text/plain',
        #                                                   delivery_mode=2))
        # fpika.return_channel(ch)
    elif action == 'play':
        common_network_pika.com_net_pika_send({'Type': 'Play', 'Subtype': 'Cast',
                                               'User': current_user.get_id(),
                                               'Data': g.db_connection.db_read_media(guid)['mm_media_path'],
                                               'Target': '10.0.0.220'},
                                              rabbit_host_name='mkrabbitmq',
                                              exchange_name='mkque_ex',
                                              route_key='mkque')
        # ch = fpika.channel()
        # ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
        #                  body=json.dumps({'Type': 'Play', 'Subtype': 'Cast',
        #                                   'User': current_user.get_id(),
        #                                   'Data': g.db_connection.db_read_media(guid)[
        #                                       'mm_media_path'],
        #                                   'Target': '10.0.0.220'}),
        #                  properties=fpika.BasicProperties(content_type='text/plain',
        #                                                   delivery_mode=2))
        # fpika.return_channel(ch)
    elif action == 'pause':
        common_network_pika.com_net_pika_send({'Type': 'Pause', 'Subtype': 'Cast',
                                               'User': current_user.get_id()},
                                              rabbit_host_name='mkrabbitmq',
                                              exchange_name='mkque_ex',
                                              route_key='mkque')
        # ch = fpika.channel()
        # ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
        #                  body=json.dumps({'Type': 'Pause', 'Subtype': 'Cast',
        #                                   'User': current_user.get_id()}),
        #                  properties=fpika.BasicProperties(content_type='text/plain',
        #                                                   delivery_mode=2))
        # fpika.return_channel(ch)
        #    elif action == 'ff':
        #        pass
    elif action == 'forward':
        pass
    elif action == 'mute':
        common_network_pika.com_net_pika_send({'Type': 'Mute', 'Subtype': 'Cast',
                                               'User': current_user.get_id()},
                                              rabbit_host_name='mkrabbitmq',
                                              exchange_name='mkque_ex',
                                              route_key='mkque')
        # ch = fpika.channel()
        # ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
        #                  body=json.dumps({'Type': 'Mute', 'Subtype': 'Cast',
        #                                   'User': current_user.get_id()}),
        #                  properties=fpika.BasicProperties(content_type='text/plain',
        #                                                   delivery_mode=2))
        # fpika.return_channel(ch)
    elif action == 'vol_up':
        common_network_pika.com_net_pika_send({'Type': 'Volume Up', 'Subtype': 'Cast',
                                               'User': current_user.get_id()},
                                              rabbit_host_name='mkrabbitmq',
                                              exchange_name='mkque_ex',
                                              route_key='mkque')
        # ch = fpika.channel()
        # ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
        #                  body=json.dumps({'Type': 'Volume Up', 'Subtype': 'Cast',
        #                                   'User': current_user.get_id()}),
        #                  properties=fpika.BasicProperties(content_type='text/plain',
        #                                                   delivery_mode=2))
        # fpika.return_channel(ch)
    elif action == 'vol down':
        common_network_pika.com_net_pika_send({'Type': 'Volume Down', 'Subtype': 'Cast',
                                               'User': current_user.get_id()},
                                              rabbit_host_name='mkrabbitmq',
                                              exchange_name='mkque_ex',
                                              route_key='mkque')
        # ch = fpika.channel()
        # ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
        #                  body=json.dumps({'Type': 'Volume Down', 'Subtype': 'Cast',
        #                                   'User': current_user.get_id()}),
        #                  properties=fpika.BasicProperties(content_type='text/plain',
        #                                                   delivery_mode=2))
        # fpika.return_channel(ch)
    return render_template("users/user_playback_cast.html", data_guid=guid,
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
