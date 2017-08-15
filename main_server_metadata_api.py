'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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
import os
import logging
import subprocess
import json
from build_image_directory import build_image_dirs
from build_trailer_directory import build_trailer_dirs
from common import common_logging
from common import common_metadata_limiter
from common import common_signal
from twisted.internet import reactor, protocol, stdio, defer, task
import pika
from pika import exceptions
from pika.adapters import twisted_connection


@defer.inlineCallbacks
def run(connection):
    channel = yield connection.channel()
    exchange = yield channel.exchange_declare(exchange='mkque_metadata_ex', type='direct', durable=True)
    queue = yield channel.queue_declare(queue='mkque_metadata', durable=True)
    yield channel.queue_bind(exchange='mkque_metadata_ex', queue='mkque_metadata')
    yield channel.basic_qos(prefetch_count=1)
    queue_object, consumer_tag = yield channel.basic_consume(queue='mkque_metadata', no_ack=False)
    l = task.LoopingCall(read, queue_object)
    l.start(0.01)


@defer.inlineCallbacks
def read(queue_object):
    logging.info('here I am in metadata consume - read')
    ch, method, properties, body = yield queue_object.get()
    if body:
        logging.info("body %s", body)
        json_message = json.loads(body)
        subprocess_command = []
        if json_message['Type'] == 'Update':
            if json_message['Sub'] == 'themoviedb':
                subprocess_command.append('python', './mediakraken/subprogram_metadata_tmdb_updates.py')
            elif json_message['Sub'] == 'thetvdb':
                subprocess_command.append('python', './mediakraken/subprogram_metadata_thetvdb_updates.py')
            elif json_message['Sub'] == 'tvmaze':
                subprocess_command.append('python', './mediakraken/subprogram_metadata_tvmaze_updates.py')
            elif json_message['Sub'] == 'collections':
                subprocess_command.append('python', './mediakraken/subprogram_metadata_update_create_collections.py')
        elif json_message['Type'] == 'Cron Run':
            # run whatever is passed in data
            subprocess_command.append('python', json_message['Data'])
        # if command list populated, run job
        if len(subprocess_command) != 0:
            subprocess.Popen(subprocess_command)
    yield ch.basic_ack(delivery_tag=method.delivery_tag)


# TODO should be using env variables
# build image directories if needed
if os.path.isdir('/mediakraken/web_app/MediaKraken/static/meta/images/backdrop/a'):
    pass
else:
    build_image_dirs()


# TODO should be using env variables
# build trailer directories if needed
if os.path.isdir('/mediakraken/web_app/MediaKraken/static/meta/trailers/trailer/a'):
    pass
else:
    build_trailer_dirs()


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Metadata_API')


# fire off wait for it script to allow rabbitmq connection
wait_pid = subprocess.Popen(['/mediakraken/wait-for-it-ash.sh', '-h',
                             'mkrabbitmq', '-p', ' 5672'], shell=False)
wait_pid.wait()


# pika rabbitmq connection
parameters = pika.ConnectionParameters(credentials=pika.PlainCredentials('guest', 'guest'))
cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, parameters)
d = cc.connectTCP('mkrabbitmq', 5672)
d.addCallback(lambda protocol: protocol.ready)
d.addCallback(run)


# fire up the workers for each provider
for meta_provider in common_metadata_limiter.API_LIMIT.keys():
    logging.info("meta_provider: %s", meta_provider)
    proc_api_fetch = subprocess.Popen(['python', './main_server_metadata_api_worker.py',
                                       meta_provider], shell=False)


# fire up the image downloader
proc_image_fetch = subprocess.Popen(['python', './main_server_metadata_api_worker_image.py'],
                                    shell=False)
proc_image_fetch.wait() # so this doesn't end which will cause docker to restart
