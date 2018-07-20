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

import datetime
import subprocess
import time

import psutil
from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_cron_checker')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# start loop for cron checks
pid_dict = {}  # pylint: disable=C0103
while 1:
    for row_data in db_connection.db_cron_list(True):  # only grab enabled ones
        # place holders for pid
        if row_data['mm_cron_name'] in pid_dict:
            pass
        else:
            pid_dict[row_data['mm_cron_name']] = - \
                9999999  # fake pid so it can't be found
        time_frame = None
        if row_data['mm_cron_schedule'] == "Weekly":  # chedule
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
        # check to see if cron need to process
        if row_data['mm_cron_last_run'] < date_check:
            if not psutil.pid_exists(pid_dict[row_data['mm_cron_name']]):
                if row_data['mm_cron_file_path'][-3:] == '.py':
                    proc = subprocess.Popen(['python3', row_data['mm_cron_file_path']],
                                            shell=False)
                else:
                    proc = subprocess.Popen(['/usr/sbin', row_data['mm_cron_file_path']],
                                            shell=False)
                    common_global.es_inst.com_elastic_index('info',
                                                   {'cron': row_data['mm_cron_name'],
                                                    'pid': proc.pid})
                db_connection.db_cron_time_update(row_data['mm_cron_name'])
                pid_dict[row_data['mm_cron_name']] = proc.pid
            # commit off each match
            db_connection.db_commit()
            common_global.es_inst.com_elastic_index('info', {'data': row_data})
    time.sleep(60)  # sleep for 60 seconds

# close the database
db_connection.db_close()
