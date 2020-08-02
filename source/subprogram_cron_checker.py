"""
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
"""

import datetime
import json
import time

import pika
from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_network
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_cron_checker')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# fire off wait for it script to allow connection
common_network.mk_network_service_available('mkstack_rabbitmq', '5672')

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('mkstack_rabbitmq',
                                       socket_timeout=30, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# start loop for cron checks
while 1:
    for row_data in db_connection.db_cron_list(True):  # only grab enabled ones
        time_frame = None
        if row_data['mm_cron_schedule'] == "Weekly":  # schedule
            time_frame = datetime.timedelta(weeks=1)
        elif row_data['mm_cron_schedule'].split(' ', 1)[0] == "Days":
            time_frame = datetime.timedelta(
                days=int(row_data['mm_cron_schedule'].split(' ', 1)[1]))
        elif row_data['mm_cron_schedule'].split(' ', 1)[0] == "Hours":
            time_frame = datetime.timedelta(
                hours=int(row_data['mm_cron_schedule'].split(' ', 1)[1]))
        elif row_data['mm_cron_schedule'].split(' ', 1)[0] == "Minutes":
            time_frame = datetime.timedelta(
                minutes=int(row_data['mm_cron_schedule'].split(' ', 1)[1]))
        date_check = datetime.datetime.now() - time_frame
        # check to see if cron needs to process
        if row_data['mm_cron_last_run'] < date_check:
            channel.basic_publish(exchange=row_data['mm_cron_json']['exchange_key'],
                                  routing_key=row_data['mm_cron_json']['route_key'],
                                  body=json.dumps(
                                      {'type': row_data['mm_cron_json']['type'],
                                       'JSON': row_data['mm_cron_json']}),
                                  properties=pika.BasicProperties(
                                      content_type='text/plain',
                                      delivery_mode=2)
                                  )
            db_connection.db_cron_time_update(row_data['mm_cron_name'])
            # commit off each match
            db_connection.db_commit()
            common_global.es_inst.com_elastic_index('info', {'data': row_data})
    time.sleep(60)  # sleep for 60 seconds

# close the pika connection
connection.close()
# close the database
db_connection.db_close()
