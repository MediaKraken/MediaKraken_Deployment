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
import logging # pylint: disable=W0611
import sys
from common import common_config_ini
from common import common_file
from common import common_logging
from common import common_network_twitch
import os
import signal
import subprocess
import datetime


# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'LiveStream', False, False, None)


def signal_receive(signum, frame):
    print('CHILD LiveStream: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db_connection.db_rollback()
    db_connection.db_close()
    sys.stdout.flush()
    sys.exit(0)


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_LiveStream')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server LiveStream Start', None,\
    'System: Server LiveStream Start', 'ServerLiveStreamStart', None, None, 'System')


# grab some dirs to scan and thread out the scans
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c # pylint: disable=E1101
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# do the actual capture
filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + user + " - "\
    + (info['stream']).get("channel").get("status") + ".flv"
filename = format_filename(filename)
subprocess.call(["livestreamer", "twitch.tv/"+user, quality, "-o", filename])


# log end
db_connection.db_activity_insert('MediaKraken_Server LiveStream Stop', None,\
    'System: Server LiveStream Stop', 'ServerLiveStreamStop', None, None, 'System')

# commit all changes
db_connection.db_commit()

# close the database
db_connection.db_close()

# remove pid
os.remove(pid_file)
