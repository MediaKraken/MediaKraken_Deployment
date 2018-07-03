'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

import json
import subprocess
import time

import pika
from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_network

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_cloud')


def on_message(channel, method_frame, header_frame, body):
    """
    Process pika message
    """
    if body is not None:
        json_message = json.loads(body)
        common_global.es_inst.es_index('info', {'cloud': json_message})
        if json_message['Type'] == 'Download':
            if json_message['Sub'] == 'File':
                common_network.mk_network_fetch_from_url(json_message['URL'],
                                                         json_message['Local'])
            elif json_message['Sub'] == 'Youtube':
                dl_pid = subprocess.Popen(['youtube-dl', '-i', '--download-archive',
                                           '/mediakraken/archive.txt', json_message['Data']],
                                          shell=False)
                dl_pid.wait()  # TODO - do I really need to wait for finish?
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

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
exchange = channel.exchange_declare(exchange="mkque_cloud_ex", exchange_type="direct",
                                    durable=True)
queue = channel.queue_declare(queue='mkcloud', durable=True)
channel.queue_bind(exchange="mkque_cloud_ex", queue='mkcloud')
channel.basic_qos(prefetch_count=1)

while True:
    time.sleep(1)
    # grab message from rabbitmq if available
    try:  # since can get connection drops
        method_frame, header_frame, body = channel.basic_get(
            queue='mkcloud', no_ack=False)
        on_message(channel, method_frame, header_frame, body)
    except:
        pass

# Cancel the consumer and return any pending messages
channel.cancel()
# close the pika connection
connection.close()

# commit
db_connection.db_commit()

# close the database
db_connection.db_close()
