'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

import json
import subprocess
import time

import pika
from common import common_global
from common import common_logging_elasticsearch
from common import common_network

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_download')


def on_message(channel, method_frame, header_frame, body):
    """
    Process pika message
    """
    if body is not None:
        common_global.es_inst.com_elastic_index('info', {'msg body': body})
        json_message = json.loads(body)
        if json_message['Type'] == 'youtube':
            dl_pid = subprocess.Popen(['youtube-dl', '-i', '--download-archive',
                                       '/mediakraken/archive.txt', json_message['Data']],
                                      shell=False)
            dl_pid.wait()
        if json_message['Type'] == 'image':
            common_network.mk_network_fetch_from_url(json_message['URL'],
                                                     json_message['Local'])
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

# fire off wait for it script to allow rabbitmq connection
wait_pid = subprocess.Popen(['/mediakraken/wait-for-it-ash.sh', '-h',
                             'mkrabbitmq', '-p', ' 5672'], shell=False)
wait_pid.wait()

# pika rabbitmq connection
parameters = pika.ConnectionParameters('mkrabbitmq',
                                       credentials=pika.PlainCredentials('guest', 'guest'))
connection = pika.BlockingConnection(parameters)

# setup channels and queue
channel = connection.channel()
exchange = channel.exchange_declare(exchange="mkque_download_ex", exchange_type="direct",
                                    durable=True)
queue = channel.queue_declare(queue='mkdownload', durable=True)
channel.queue_bind(exchange="mkque_download_ex", queue='mkdownload')
channel.basic_qos(prefetch_count=1)

while True:
    time.sleep(1)
    # grab message from rabbitmq if available
    try:  # since can get connection drops
        method_frame, header_frame, body = channel.basic_get(
            queue='mkdownload', no_ack=False)
        on_message(channel, method_frame, header_frame, body)
    except:
        pass

# close the pika connection
connection.cancel()
