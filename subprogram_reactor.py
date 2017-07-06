'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
from twisted.internet import ssl
from twisted.internet import reactor
from twisted.internet.protocol import Factory
import pika
from pika import exceptions
from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol,task
from network import network_base as network_base
from network import network_base_amqp as network_amqp
from common import common_config_ini
from common import common_docker
from common import common_logging
from common import common_signal
import time
import subprocess
import json
import uuid

mk_containers = {}
docker_inst = common_docker.CommonDocker()

@defer.inlineCallbacks
def run(connection):
    channel = yield connection.channel()
    exchange = yield channel.exchange_declare(exchange='mkque_ex', type='direct', durable=True)
    queue = yield channel.queue_declare(queue='mkque', durable=True)
    yield channel.queue_bind(exchange='mkque_ex', queue='mkque')
    yield channel.basic_qos(prefetch_count=1)
    queue_object, consumer_tag = yield channel.basic_consume(queue='mkque', no_ack=False)
    l = task.LoopingCall(read, queue_object)
    l.start(0.01)


@defer.inlineCallbacks
def read(queue_object):
    global mk_containers
    logging.info('here I am in consume - read')
    ch, method, properties, body = yield queue_object.get()
    if body:
        logging.info("body %s", body)
        #network_base.NetworkEvents.ampq_message_received(body)
        json_message = json.loads(body)
        logging.info('json body %s', json_message)
        if json_message['Type'] == 'Pause':
            if json_message['Sub'] == 'Cast':
                pass
        elif json_message['Type'] == 'Play':
            # to address the 30 char name limit for container
            name_container = ((json_message['User'] + '_' + str(uuid.uuid4()).replace('-',''))[-30:])
            logging.info('cont %s', name_container)
            # TODO only for now until I get the device for websessions (cookie perhaps?)
            if 'Device' in json_message:
                define_new_container = (name_container, json_message['Device'],
                                        json_message['Target'], json_message['Data'])
            else:
                define_new_container = (name_container, None,
                                        json_message['Target'], json_message['Data'])
            logging.info('def %s', define_new_container)
            if json_message['User'] in mk_containers:
                user_activity_list = mk_containers[json_message['User']]
                user_activity_list.append(define_new_container)
                mk_containers[json_message['User']] = user_activity_list
            else:
                # "double list" so each one is it's own instance
                mk_containers[json_message['User']] = (define_new_container)
            logging.info('dict %s', mk_containers)
            if json_message['Sub'] == 'Cast':
                # should only need to check for subs on initial play command
                if 'Subtitle' in json_message:
                    subtitle_command = ' -subtitles ' + json_message['Subtitle']\
                                       + ' -subtitles_language ' + json_message['Language']
                else:
                    subtitle_command = ''
                logging.info('b4 cast run')
                try:
                    docker_inst.com_docker_run_container(container_name=name_container,
                        container_command=('python /mediakraken/stream2chromecast/stream2chromecast.py'
                        + ' -devicename ' + json_message['Target']
                        + subtitle_command + ' -transcodeopts \'-c:v copy -c:a ac3'
                        + ' -movflags faststart+empty_moov\' -transcode \'' + json_message['Data'] + '\''))
                except Exception as e:
                    logging.error('cast ex %s', str(e))
                logging.info('after cast run')
            else:
                logging.info('b4 run')
                docker_inst.com_docker_run_container(container_name=name_container,
                     container_command=(
                        'ffmpeg -i \'' + json_message['Data'] + '\''))
                logging.info('after run')
        elif json_message['Type'] == 'Stop':
            pass
    yield ch.basic_ack(delivery_tag=method.delivery_tag)


class MediaKrakenServerApp(Factory):
    def __init__(self):
        # start logging
        common_logging.com_logging_start('./log/MediaKraken_Subprogram_Reactor')
        # set other data
        self.server_start_time = time.mktime(time.gmtime())
        self.users = {} # maps user names to network instances
        self.option_config_json, self.db_connection = common_config_ini.com_config_read()
        logging.info("Ready for connections!")


    def buildProtocol(self, addr):
        return network_base.NetworkEvents(self.users, self.db_connection)


if __name__ == '__main__':
    # set signal exit breaks
    common_signal.com_signal_set_break()

    # fire off wait for it script to allow rabbitmq connection
    wait_pid = subprocess.Popen(['/mediakraken/wait-for-it-ash.sh', '-h', 'mkrabbitmq', '-p', ' 5672'], shell=False)
    wait_pid.wait()

    # pika rabbitmq connection
    parameters = pika.ConnectionParameters(credentials=pika.PlainCredentials('guest', 'guest'))
    cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, parameters)
    d = cc.connectTCP('mkrabbitmq', 5672)
    d.addCallback(lambda protocol: protocol.ready)
    d.addCallback(run)

    # setup for the ssl keys
    reactor.listenSSL(8903, MediaKrakenServerApp(),
                      ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
    reactor.run()
