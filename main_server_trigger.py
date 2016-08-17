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
import ConfigParser
CONFIG_HANDLE = ConfigParser.ConfigParser()
CONFIG_HANDLE.read("MediaKraken.ini")
import sys
from common import common_logging
import subprocess
import signal
import os
import time
import database as database_base
try:
    import cPickle as pickle
except:
    import pickle


def signal_receive(signum, frame):
    print('CHILD Main Trigger: Received USR1')
    os.kill(proc_trigger.pid, signal.SIGTERM)
    # cleanup db
    db.srv_db_rollback()
    # log stop
    db.srv_db_activity_insert('MediaKraken_Trigger Stop', None,\
        'System: Trigger Stop', 'ServerTriggerStop', None, None, 'System')
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)


# store pid for initd
pid = os.getpid()
op = open("/var/mm_server_trigger.pid", "w")
op.write("%s" % pid)
op.close()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Trigger')


# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(CONFIG_HANDLE.get('DB Connections', 'PostDBHost').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBPort').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBName').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBUser').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBPass').strip())


db.srv_db_activity_insert('MediaKraken_Trigger Start', None, 'System: Trigger Start',\
    'ServerTriggerStart', None, None, 'System')


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


while True:
    # check for new "triggers"
    for row_data in db.srv_db_triggers_read():
        # fire up cron service
        command_list = []
        for command_data in pickle.loads(str(row_data[1])):
            command_list.append(command_data)
        proc_trigger = subprocess.Popen(command_list, shell=False)
        logging.debug("Trigger PID: %s", proc_trigger.pid)
        # remove trigger from DB
        db.srv_db_triggers_delete(row_data[0])
    time.sleep(1)


# log stop
db.srv_db_activity_insert('MediaKraken_Trigger Stop', None,\
    'System: Trigger Stop', 'ServerTriggerStop', None, None, 'System')


# commit
db.srv_db_commit()


# close the database
db.srv_db_close()


# stop children
os.kill(proc_trigger.pid, signal.SIGTERM)
