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
import os
import signal
sys.path.append("../common")
sys.path.append("../server")
from common import common_file
from common import common_logging
import database as database_base

def signal_receive(signum, frame):
    print('CHILD URL Check: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_Rollback()
    db.srv_db_Close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c

# start logging
common_logging.common_logging_Start('./log/MediaKraken_Subprogram_URL_Checker')

# open the database
db = database_base.MK_Server_Database()
db.srv_db_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_Activity_Insert('MediaKraken_Server URL Scan Start', None,\
    'System: Server URL Scan Start', 'ServerURLScanStart', None, None, 'System')

# go through ALL known media files
for row_data in db.srv_db_Known_Media():

#TODO  actually, this should probably be the metadata

    logging.debug(row_data)



# log end
db.srv_db_Activity_Insert('MediaKraken_Server URL Scan Stop', None,\
    'System: Server URL Scan Stop', 'ServerURLScanStop', None, None, 'System')

# commit all changes to db
db.srv_db_Commit()

# close DB
db.srv_db_Close()
