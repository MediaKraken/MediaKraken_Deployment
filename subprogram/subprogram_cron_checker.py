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

# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import logging
import sys
sys.path.append("./")  # for db import
sys.path.append("../MediaKraken_Common")
import MK_Common_File
import MK_Common_Logging
import database as database_base
import datetime
import time
import os
import signal
import psutil
import subprocess
import signal

# create the file for pid
pid_file = './pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'Sub_Cron_Checker', False, False, None)

def signal_receive(signum, frame):
    print 'CHILD Cron: Received USR1'
    # term all running crons
    if row_data[1] in pid_dict:
        os.kill(row_data[1], signal.SIGTERM)
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)

# grab some dirs to scan and thread out the scans
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_Cron')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())


# start loop for cron checks
pid_dict = {}
while 1:
    for row_data in db.MK_Server_Database_Cron_List(True):  # only grab enabled ones
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
                db.MK_Server_Database_Cron_Time_Update(row_data['mm_cron_name'])
                pid_dict[row_data['mm_cron_name']] = proc.pid
            # commit off each match
            db.MK_Server_Database_Commit()
        logging.debug(row_data)
    time.sleep(60)  # sleep for 60 seconds

# close the database
db.MK_Server_Database_Close()

# remove pid
os.remove(pid_file)
