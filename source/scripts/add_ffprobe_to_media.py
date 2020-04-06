"""
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
"""

import json

import pika
from common import common_config_ini
from common import common_network

# fire off wait for it script to allow connection
common_network.mk_network_service_available('mkstack_rabbitmq', '5672')

# Open a connection to RabbitMQ on localhost using all default parameters
connection = pika.BlockingConnection()

# Open the channel
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue="mkffmpeg", durable=True,
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
        channel.basic_publish(exchange='mkque_ffmpeg_ex',
                              routing_key='mkffmpeg',
                              body=json.dumps(
                                  {'Type': 'FFMPEG', 'Data': media['mm_media_guid']}),
                              properties=pika.BasicProperties(content_type='text/plain',
                                                              delivery_mode=2))

# Cancel the consumer and return any pending messages
channel.cancel()
connection.close()

# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
