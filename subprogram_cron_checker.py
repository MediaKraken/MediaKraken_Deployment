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
from common import common_file
from common import common_logging
from server import database as database_base
import datetime
import time
import os
import signal
import psutil
import subprocess
import signal

# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Sub_Cron_Checker', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Cron: Received USR1')
    # term all running crons
    if row_data[1] in pid_dict:
        os.kill(row_data[1], signal.SIGTERM)
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_rollback()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)

# grab some dirs to scan and thread out the scans
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Cron')


# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(CONFIG_HANDLE.get('DB Connections', 'PostDBHost').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBPort').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBName').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBUser').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBPass').strip())


# start loop for cron checks
pid_dict = {}
while 1:
    for row_data in db.srv_db_cron_list(True):  # only grab enabled ones
        # place holders for pid
        if row_data['mm_cron_name'] in pid_dict:
            pass
        else:
            pid_dict[row_data['mm_cron_name']] = -9999999 # fake pid so it can't be found
        time_frame = None
        if row_data['mm_cron_schedule'] == "Weekly":  # chedule
            time_frame = datetime.timedelta(weeks=1)
        elif row_data['mm_cron_schedule'].split(' ', 1)[0] == "Days":
            time_frame = datetime.timedelta(days=int(row_data['mm_cron_schedule'].split(' ', 1)[1]))
        elif row_data['mm_cron_schedule'].split(' ', 1)[0] == "Hours":
            time_frame = datetime.timedelta(hours=int(row_data['mm_cron_schedule'].split(' ', 1)[1]))
        elif row_data['mm_cron_schedule'].split(' ', 1)[0] == "Minutes":
            time_frame = datetime.timedelta(minutes=int(row_data['mm_cron_schedule'].split(' ', 1)[1]))
        date_check = datetime.datetime.now() - time_frame
        # check to see if cron need to process
        if row_data['mm_cron_last_run'] < date_check:
            if not psutil.pid_exists(pid_dict[row_data['mm_cron_name']]):
                if row_data['mm_cron_file_path'][-3:] == '.py':
                    proc = subprocess.Popen(['python', row_data['mm_cron_file_path']], shell=False)
                else:
                    proc = subprocess.Popen(['/usr/sbin', row_data['mm_cron_file_path']], shell=False)
                logging.debug("Cron $s PID %s:", row_data['mm_cron_name'], proc.pid)
                db.srv_db_cron_time_update(row_data['mm_cron_name'])
                pid_dict[row_data['mm_cron_name']] = proc.pid
            # commit off each match
            db.srv_db_commit()
        logging.debug(row_data)
    time.sleep(60) # sleep for 60 seconds

# close the database
db.srv_db_close()

# remove pid
os.remove(pid_file)
