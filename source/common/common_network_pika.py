"""
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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


def com_net_pika_send(body_data, rabbit_host_name='mkstack_rabbitmq', exchange_name='mkque_ex',
                      route_key='mkque'):
    pika_inst = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host_name))
    pika_channel = pika_inst.channel()
    pika_channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
    pika_channel.basic_publish(exchange=exchange_name,
                               routing_key=route_key,
                               body=json.dumps(body_data),
                               properties=pika.BasicProperties(content_type='text/plain',
                                                               delivery_mode=2))
    pika_inst.close()
