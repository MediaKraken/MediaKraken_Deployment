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
sys.path.append("../MediaKraken_Common")
import MK_Common_Logging
import MK_Common_Roku
sys.path.append("../MediaKraken_Server")
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

def signal_receive(signum, frame):
    print('CHILD Roku Thumbnail: Received USR1')
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
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_Roku_Thumbnail')

# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())

# log start
db.MK_Server_Database_Activity_Insert('MediaKraken_Server Roku Thumbnail Generate Start', None,\
    'System: Server Roku Thumbnail Generate Start', 'ServerRokuThumbStart', None, None, 'System')

# go through ALL known media files
thumbnails_generated = 0
for row_data in db.MK_Server_Database_Known_Media():

#TODO  actually, this should probably be the metadata
# TODO the common roku code has the bif/thumb gen

    logging.debug(row_data)


# send notications
if thumbnails_generated > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', thumbnails_generated, True) + " Roku thumbnail(s) generated.", True)

# log end
db.MK_Server_Database_Activity_Insert('MediaKraken_Server Roku Thumbnail Generate Stop', None,\
    'System: Server Roku Thumbnail Generate Stop', 'ServerRokuThumbStop', None, None, 'System')

# commit all changes
db.MK_Server_Database_Commit()

# close DB
db.MK_Server_Database_Close()
