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
import time
import os
from common import common_config_ini
from common import common_cloud
from common import common_logging

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Postgresql_Backup')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read(True)


# log start
db_connection.db_activity_insert('MediaKraken_Server Postgresql Backup Start', None,\
    'System: Server DB Backup Start', 'ServerBackupStart', None, None, 'System')


# generate dump file
backup_file_name = 'MediaKraken_Backup_' + time.strftime("%Y%m%d%H%M%S") + '.dump'
os.system('PGPASSWORD=' + config_handle['DB Connections']['PostDBPass']\
    + ' pg_dump -U '\
    + config_handle['DB Connections']['PostDBUser'] + ' '\
    + config_handle['DB Connections']['PostDBName'] + ' -F c -f '\
    + config_handle['MediaKrakenServer']['BackupLocal'] + '/' + backup_file_name)

# grab settings and options
option_json = db_connection.db_opt_status_read()['mm_options_json']
if option_json['Backup']['BackupType'] != 'local':
    common_cloud.com_cloud_file_store(option_json['Backup']['BackupType'],\
    config_handle['MediaKrakenServer']['BackupLocal'] + '/'\
    + backup_file_name, backup_file_name, True)

# log end
db_connection.db_activity_insert('MediaKraken_Server Postgresql Backup Stop', None,\
    'System: Server DB Backup Stop', 'ServerBackupStop', None, None, 'System')

# commit records
db_connection.db_commit()

# close the database
db_connection.db_close()
