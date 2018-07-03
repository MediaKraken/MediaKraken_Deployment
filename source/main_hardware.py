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
from common import common_global
from common import common_hardware_hue
from common import common_logging_elasticsearch

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_hardware')


def on_message(channel, method_frame, header_frame, body):
    """
    Process pika message
    """
    if body is not None:
        json_message = json.loads(body)
        common_global.es_inst.es_index('info', {'hardware': json_message})
        if json_message['Type'] == 'Lights':
            hardware_hue = common_hardware_hue.CommonHardwareHue(json_message['Target'])
            if json_message['Sub'] == 'OnOff':
                hardware_hue.com_hardware_hue_light_set(json_message['LightList'], 'on',
                                                        json_message['Data'])
            elif json_message['Sub'] == 'Bright':
                hardware_hue.com_hardware_hue_light_set(json_message['LightList'], 'bri',
                                                        json_message['Data'])
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
exchange = channel.exchange_declare(exchange="mkque_hardware_ex", exchange_type="direct",
                                    durable=True)
queue = channel.queue_declare(queue='mkhardware', durable=True)
channel.queue_bind(exchange="mkque_hardware_ex", queue='mkhardware')
channel.basic_qos(prefetch_count=1)

while True:
    time.sleep(1)
    # grab message from rabbitmq if available
    try:  # since can get connection drops
        method_frame, header_frame, body = channel.basic_get(
            queue='mkhardware', no_ack=False)
        on_message(channel, method_frame, header_frame, body)
    except:
        pass

# close the pika connection
connection.close()
