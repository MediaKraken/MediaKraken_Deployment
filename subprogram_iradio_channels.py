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
from common import common_network_radio
import os
import signal
import database as database_base


# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Sub_iRadio', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Cron: Received USR1')
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
common_logging.com_logging_start('./log/MediaKraken_Subprogram_IRadio')

# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(CONFIG_HANDLE.get('DB Connections', 'PostDBHost').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBPort').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBName').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBUser').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_activity_insert('MediaKraken_Server iRadio Start', None,\
    'System: Server iRadio Start', 'ServeriRadioStart', None, None, 'System')

# start code for updating iradio database
#common_network_Radio.com_network_Radio()

# load the cache files and compare to db
radio_cache = common_file.com_file_load_data('./cache.pickle', True)
for row_data in radio_cache:
    logging.debug(row_data)
    db.srv_db_iradio_insert(row_data)

#radio_xiph = common_file.com_file_load_data('./xiph.pickle', True)

# log end
db.srv_db_activity_insert('MediaKraken_Server iRadio Stop', None,\
    'System: Server iRadio Stop', 'ServeriRadioStop', None, None, 'System')

# commit
db.srv_db_commit()

# close the database
db.srv_db_close()

# remove pid
os.remove(pid_file)
