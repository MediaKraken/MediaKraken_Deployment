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

import json
import subprocess
import time

import pika
from common import common_config_ini
from common import common_ffmpeg
from common import common_global
from common import common_logging_elasticsearch

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_ffprobe')


def on_message(channel, method_frame, header_frame, body):
    """
    Process pika message
    """
    if body is not None:
        json_message = json.loads(body)
        common_global.es_inst.es_index('info', {'ffprobe': json_message})
        db_connection.db_media_ffmeg_update(json_message['Data'],
                                            json.dumps(common_ffmpeg.com_ffmpeg_media_attr(
                                                db_connection.db_read_media(
                                                    json_message['Data'])['mm_media_path'])))
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
exchange = channel.exchange_declare(exchange="mkque_ffmpeg_ex", exchange_type="direct",
                                    durable=True)
queue = channel.queue_declare(queue='mkffmpeg', durable=True)
channel.queue_bind(exchange="mkque_ffmpeg_ex", queue='mkffmpeg')
channel.basic_qos(prefetch_count=1)

while True:
    time.sleep(1)
    # grab message from rabbitmq if available
    try:  # since can get connection drops
        method_frame, header_frame, body = channel.basic_get(
            queue='mkffmpeg', no_ack=False)
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
