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

import sys
sys.path.append("../MediaKraken_Common")
sys.path.append("./")  # for db import
import MK_Common_File
import MK_Common_Logging
import MK_Common_Twitch
import os
import signal
import database as database_base
import logging
import subprocess
import datetime


# create the file for pid
pid_file = './pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'LiveStream', False, False, None)


def signal_receive(signum, frame):
    global global_end_program
    global_end_program = True
    print 'CHILD LiveStream: Received USR1'
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_LiveStream')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server LiveStream Start', None, u'System: Server LiveStream Start', u'ServerLiveStreamStart', None, None, u'System')


# grab some dirs to scan and thread out the scans
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# do the actual capture
filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - "+user+" - "+(info['stream']).get("channel").get("status")+".flv"
filename = format_filename(filename)
subprocess.call(["livestreamer", "twitch.tv/"+user, quality, "-o", filename])


# log end
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server LiveStream Stop', None, u'System: Server LiveStream Stop', u'ServerLiveStreamStop', None, None, u'System')

# commit all changes
db.MK_Server_Database_Commit()

# close the database
db.MK_Server_Database_Close()

# remove pid
os.remove(pid_file)
