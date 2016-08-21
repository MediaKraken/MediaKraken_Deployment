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
import sys
import os
import signal
from common import common_config_ini
from common import common_logging
from common import common_hardware_roku
import locale
locale.setlocale(locale.LC_ALL, '')

def signal_receive(signum, frame):
    print('CHILD Roku Thumbnail: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db_connection.db_rollback()
    db_connection.db_close()
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
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Roku Thumbnail Generate Start', None,\
    'System: Server Roku Thumbnail Generate Start', 'ServerRokuThumbStart', None, None, 'System')

# go through ALL known media files
thumbnails_generated = 0
for row_data in db_connection.db_known_media():

#TODO  actually, this should probably be the metadata
# TODO the common roku code has the bif/thumb gen

    logging.debug(row_data)


# send notications
if thumbnails_generated > 0:
    db_connection.db_notification_insert(locale.format('%d', thumbnails_generated, True)\
        + " Roku thumbnail(s) generated.", True)

# log end
db_connection.db_activity_insert('MediaKraken_Server Roku Thumbnail Generate Stop', None,\
    'System: Server Roku Thumbnail Generate Stop', 'ServerRokuThumbStop', None, None, 'System')

# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
