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

import pika
from common import common_config_ini

# fire off wait for it script to allow rabbitmq connection
wait_pid = subprocess.Popen(['/mediakraken/wait-for-it-ash.sh', '-h',
                             'mkrabbitmq', '-p', ' 5672'], shell=False)
wait_pid.wait()

# Open a connection to RabbitMQ on localhost using all default parameters
connection = pika.BlockingConnection()

# Open the channel
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue="mkque", durable=True,
                      exclusive=False, auto_delete=False)

# Turn on delivery confirmations
channel.confirm_delivery()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# loop through all media
for media in db_connection.db_read_media():
    print(('media: %s' % media))
    if media['mm_media_ffprobe_json'] is None:
        # Send a message so ffprobe runs
        channel.basic_publish(exchange='mkque_ex',
                              routing_key='mkque',
                              body=json.dumps(
                                  {'Type': 'FFMPEG', 'Data': media['mm_media_guid']}),
                              properties=pika.BasicProperties(content_type='text/plain',
                                                              delivery_mode=1))

# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
