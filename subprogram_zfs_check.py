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
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import os
import sys
sys.path.append("../common")
sys.path.append("../server")
import database as database_base
from common import common_file
from common import common_logging
from common import common_zfs

# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.common_file_Save_Data(pid_file, 'ZFS_Health_Scan', False, False, None)

def signal_receive(signum, frame):
    global global_end_program
    global_end_program = True
    print('CHILD ZFS Health Scan: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_Rollback()
    db.srv_db_Close()
    sys.stdout.flush()
    sys.exit(0)

# start logging
common_logging.common_logging_Start('./log/MediaKraken_Subprogram_ZFS_Check')

# open the database
db = database_base.MK_Server_Database()
db.srv_db_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_Activity_Insert('MediaKraken_Server ZFS Health Start', None,\
    'System: Server ZFS Health Start', 'ServerZFSScanStart', None, None, 'System')

# health check
for read_line in common_zfs.common_zfs_Health_Check():
    if read_line.find('ONLINE') != -1:
        db.srv_db_Activity_Insert('MediaKraken_Server ZFS ERROR!', None,\
            'System: ZFS Health ERROR!', 'ServerZFSERROR', None, None, 'System')
        db.srv_db_Notification_Insert("ZFS zpool(s) degraded or offline!", True)
        break

# log end
db.srv_db_Activity_Insert('MediaKraken_Server ZFS Health Stop', None,\
    'System: Server ZFS Health Stop', 'ServerZFSScanStop', None, None, 'System')

# commit
db.srv_db_Commit()

# close the database
db.srv_db_Close()

# remove pid
os.remove(pid_file)
