'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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
import sys
sys.path.append("../common")
sys.path.append("../server")
from common import common_file
from common import common_logging
from common import common_Twitch
import os
import signal
import database as database_base
import subprocess
import datetime


# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'LiveStream', False, False, None)


def signal_receive(signum, frame):
    global global_end_program
    global_end_program = True
    print('CHILD LiveStream: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_rollback()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_LiveStream')


# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_activity_insert('MediaKraken_Server LiveStream Start', None,\
    'System: Server LiveStream Start', 'ServerLiveStreamStart', None, None, 'System')


# grab some dirs to scan and thread out the scans
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# do the actual capture
filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + user + " - "\
    + (info['stream']).get("channel").get("status") + ".flv"
filename = format_filename(filename)
subprocess.call(["livestreamer", "twitch.tv/"+user, quality, "-o", filename])


# log end
db.srv_db_activity_insert('MediaKraken_Server LiveStream Stop', None,\
    'System: Server LiveStream Stop', 'ServerLiveStreamStop', None, None, 'System')

# commit all changes
db.srv_db_commit()

# close the database
db.srv_db_close()

# remove pid
os.remove(pid_file)
