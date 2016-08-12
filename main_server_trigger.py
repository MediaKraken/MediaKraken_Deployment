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
import logging
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import sys
sys.path.append("./common")
sys.path.append("./server")
import common.common_logging
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
    db.srv_db_Rollback()
    # log stop
    db.srv_db_Activity_Insert('MediaKraken_Trigger Stop', None,\
        'System: Trigger Stop', 'ServerTriggerStop', None, None, 'System')
    db.srv_db_Close()
    sys.stdout.flush()
    sys.exit(0)


# store pid for initd
pid = os.getpid()
op = open("/var/mm_server_trigger.pid", "w")
op.write("%s" % pid)
op.close()


# start logging
common_logging.common_logging_Start('./log/MediaKraken_Trigger')


# open the database
db = database_base.MK_Server_Database()
db.srv_db_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


db.srv_db_Activity_Insert('MediaKraken_Trigger Start', None, 'System: Trigger Start',\
    'ServerTriggerStart', None, None, 'System')


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


while True:
    # check for new "triggers"
    for row_data in db.srv_db_Triggers_Read():
        # fire up cron service
        command_list = []
        for command_data in pickle.loads(str(row_data[1])):
            command_list.append(command_data)
        proc_trigger = subprocess.Popen(command_list, shell=False)
        logging.debug("Trigger PID: %s", proc_trigger.pid)
        # remove trigger from DB
        db.srv_db_Triggers_Delete(row_data[0])
    time.sleep(1)


# log stop
db.srv_db_Activity_Insert('MediaKraken_Trigger Stop', None,\
    'System: Trigger Stop', 'ServerTriggerStop', None, None, 'System')


# commit
db.srv_db_Commit()


# close the database
db.srv_db_Close()


# stop children
os.kill(proc_trigger.pid, signal.SIGTERM)
