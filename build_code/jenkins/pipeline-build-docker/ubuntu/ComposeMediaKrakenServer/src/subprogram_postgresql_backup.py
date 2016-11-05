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
from common import common_signal


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Postgresql_Backup')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Postgresql Backup Start', None,\
    'System: Server DB Backup Start', 'ServerBackupStart', None, None, 'System')


# generate dump file
backup_file_name = 'MediaKraken_Backup_' + time.strftime("%Y%m%d%H%M%S") + '.dump'
os.system('PGPASSWORD=' + config_handle.get('DB Connections', 'PostDBPass')\
    + ' pg_dump -U '\
    + config_handle.get('DB Connections', 'PostDBUser') + ' '\
    + config_handle.get('DB Connections', 'PostDBName') + ' -F c -f '\
    + os.path.join(option_config_json['MediaKrakenServer']['BackupLocal'], backup_file_name))


cloud_handle = common_cloud.CommonCloud(option_config_json)
# grab settings and options
option_json = db_connection.db_opt_status_read()['mm_options_json']
if option_json['Backup']['BackupType'] != 'local':
    cloud_handle.com_cloud_file_store(option_json['Backup']['BackupType'],\
        os.path.join(option_config_json['MediaKrakenServer']['BackupLocal'],\
        backup_file_name), backup_file_name, True)


# log end
db_connection.db_activity_insert('MediaKraken_Server Postgresql Backup Stop', None,\
    'System: Server DB Backup Stop', 'ServerBackupStop', None, None, 'System')


# commit records
db_connection.db_commit()


# close the database
db_connection.db_close()
