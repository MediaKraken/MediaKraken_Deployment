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
import sys
import logging
import os
import signal
sys.path.append("../MediaKraken_Common")
sys.path.append("./")  # for db import
import MK_Common_File
import MK_Common_Logging
import database as database_base

def signal_receive(signum, frame):
    print 'CHILD URL Check: Received USR1'
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c

# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_URL_Checker')

# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())

# log start
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server URL Scan Start', None, u'System: Server URL Scan Start', u'ServerURLScanStart', None, None, u'System')

# go through ALL known media files
for row_data in db.MK_Server_Database_Known_Media():

#TODO  actually, this should probably be the metadata

    logging.debug(row_data)



# log end
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server URL Scan Stop', None, u'System: Server URL Scan Stop', u'ServerURLScanStop', None, None, u'System')

# commit all changes to db
db.MK_Server_Database_Commit()

# close DB
db.MK_Server_Database_Close()
