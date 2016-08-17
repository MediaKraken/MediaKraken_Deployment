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
import ConfigParser
CONFIG_HANDLE = ConfigParser.ConfigParser()
CONFIG_HANDLE.read("MediaKraken.ini")
import os
import sys
import database as database_base
from common import common_file
from common import common_logging
from common import common_zfs

# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'ZFS_Health_Scan', False, False, None)

def signal_receive(signum, frame):
    global global_end_program
    global_end_program = True
    print('CHILD ZFS Health Scan: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_rollback()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_ZFS_Check')

# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(CONFIG_HANDLE.get('DB Connections', 'PostDBHost').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBPort').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBName').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBUser').strip(),\
    CONFIG_HANDLE.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_activity_insert('MediaKraken_Server ZFS Health Start', None,\
    'System: Server ZFS Health Start', 'ServerZFSScanStart', None, None, 'System')

# health check
zfs_result = common_zfs.com_zfs_health_check()
if zfs_result is not None:
    for read_line in zfs_result:
        if read_line.find('ONLINE') != -1:
            db.srv_db_activity_insert('MediaKraken_Server ZFS ERROR!', None,\
                'System: ZFS Health ERROR!', 'ServerZFSERROR', None, None, 'System')
            db.srv_db_notification_insert("ZFS zpool(s) degraded or offline!", True)
            break

# log end
db.srv_db_activity_insert('MediaKraken_Server ZFS Health Stop', None,\
    'System: Server ZFS Health Stop', 'ServerZFSScanStop', None, None, 'System')

# commit
db.srv_db_commit()

# close the database
db.srv_db_close()

# remove pid
os.remove(pid_file)
