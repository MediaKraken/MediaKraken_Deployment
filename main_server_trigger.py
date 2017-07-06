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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
from common import common_config_ini
from common import common_logging
from common import common_signal
import subprocess
import time
try:
    import cPickle as pickle
except:
    import pickle


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Trigger')


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


db_connection.db_activity_insert('MediaKraken_Trigger Start', None, 'System: Trigger Start',
    'ServerTriggerStart', None, None, 'System')


trigger_pid_list = []
while True:
    # check for new "triggers"
    for row_data in db_connection.db_triggers_read():
        # fire up cron service
        command_list = []
        for command_data in pickle.loads(str(row_data['mm_trigger_command'])):
            command_list.append(command_data)
        proc_trigger = subprocess.Popen(command_list, shell=False)
        logging.info("Trigger PID: %s", proc_trigger.pid)
        logging.info("Trigger Command %s", command_list)
        # remove trigger from DB
        db_connection.db_triggers_delete(row_data['mm_trigger_guid'])
        trigger_pid_list.append(proc_trigger.pid)
    time.sleep(1)


# log stop
db_connection.db_activity_insert('MediaKraken_Trigger Stop', None,
    'System: Trigger Stop', 'ServerTriggerStop', None, None, 'System')


# commit
db_connection.db_commit()


# close the database
db_connection.db_close()
