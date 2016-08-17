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
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
import sys
import os
import signal
sys.path.append("./common")
from common import common_logging
from common import common_Roku
sys.path.append("./server")
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

def signal_receive(signum, frame):
    print('CHILD Roku Thumbnail: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_rollback()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Roku_Thumbnail')

# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
    config_handle.get('DB Connections', 'PostDBPort').strip(),\
    config_handle.get('DB Connections', 'PostDBName').strip(),\
    config_handle.get('DB Connections', 'PostDBUser').strip(),\
    config_handle.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_activity_insert('MediaKraken_Server Roku Thumbnail Generate Start', None,\
    'System: Server Roku Thumbnail Generate Start', 'ServerRokuThumbStart', None, None, 'System')

# go through ALL known media files
thumbnails_generated = 0
for row_data in db.srv_db_known_media():

#TODO  actually, this should probably be the metadata
# TODO the common roku code has the bif/thumb gen

    logging.debug(row_data)


# send notications
if thumbnails_generated > 0:
    db.srv_db_notification_insert(locale.format('%d', thumbnails_generated, True)\
        + " Roku thumbnail(s) generated.", True)

# log end
db.srv_db_activity_insert('MediaKraken_Server Roku Thumbnail Generate Stop', None,\
    'System: Server Roku Thumbnail Generate Stop', 'ServerRokuThumbStop', None, None, 'System')

# commit all changes
db.srv_db_commit()

# close DB
db.srv_db_close()
