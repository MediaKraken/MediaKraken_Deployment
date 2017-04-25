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
from network import network_base_string as network_base
from common import common_config_ini
from common import common_logging
from common import common_signal
import time


@defer.inlineCallbacks
def run(connection):
    channel = yield connection.channel()
    exchange = yield channel.exchange_declare(exchange='mkque_ex', type='direct')
    queue = yield channel.queue_declare(queue='mkque', durable=True)
    yield channel.queue_bind(exchange='mkque_ex', queue='mkque')  # , routing_key='mkque.world')
    yield channel.basic_qos(prefetch_count=1)
    queue_object, consumer_tag = yield channel.basic_consume(queue='mkque', no_ack=False)
    l = task.LoopingCall(read, queue_object)
    l.start(0.01)


@defer.inlineCallbacks
def read(queue_object):
    ch, method, properties, body = yield queue_object.get()
    if body:
        logging.info("body %s", body)
        #network_base.NetworkEvents.broadcast_celery_message(body)
    yield ch.basic_ack(delivery_tag=method.delivery_tag)


class MediaKrakenServerApp(Factory):
    def __init__(self):
        # start logging
        common_logging.com_logging_start('./log/MediaKraken_Subprogram_Reactor_String')
        # set other data
        self.server_start_time = time.mktime(time.gmtime())
        self.users = {} # maps user names to network instances
        # preload some data from database
        self.option_config_json, self.db_connection = common_config_ini.com_config_read()
        self.genre_list = self.db_connection.db_meta_genre_list()
        logging.info("Ready for connections!")


    def buildProtocol(self, addr):
        return network_base.NetworkEvents(self.users, self.db_connection,
            self.genre_list, self.option_config_json)


if __name__ == '__main__':
    # set signal exit breaks
    common_signal.com_signal_set_break()
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
