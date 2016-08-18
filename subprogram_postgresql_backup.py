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
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
import time
import os
from common import common_cloud
from common import common_logging
import database as database_base

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Postgresql_Backup')

# open the database
db = database_base.MKServerDatabase()
db.db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
    config_handle.get('DB Connections', 'PostDBPort').strip(),\
    config_handle.get('DB Connections', 'PostDBName').strip(),\
    config_handle.get('DB Connections', 'PostDBUser').strip(),\
    config_handle.get('DB Connections', 'PostDBPass').strip())


# log start
db.db_activity_insert('MediaKraken_Server Postgresql Backup Start', None,\
    'System: Server DB Backup Start', 'ServerBackupStart', None, None, 'System')

# popen appears to be trying to execute pgpassword
#proc_back = subprocess.Popen(['PGPASSWORD=' + config_handle.get('DB Connections','PostDBPass').strip(), 'pg_dump', '-U', config_handle.get('DB Connections','PostDBUser').strip(), config_handle.get('DB Connections','PostDBName').strip(), '-F', 'c', '-f', config_handle.get('MediaKrakenServer','BackupLocal').strip() + '/MediaKraken_Backup_' + time.strftime("%Y%m%d%H%M%S") + '.dump'], shell=False)
#proc_back.pid.wait()

# generate dump file
backup_file_name = 'MediaKraken_Backup_' + time.strftime("%Y%m%d%H%M%S") + '.dump'
os.system('PGPASSWORD=' + config_handle.get('DB Connections', 'PostDBPass').strip()\
    + ' pg_dump -U '\
    + config_handle.get('DB Connections', 'PostDBUser').strip() + ' '\
    + config_handle.get('DB Connections', 'PostDBName').strip() + ' -F c -f '\
    + config_handle.get('MediaKrakenServer', 'BackupLocal').strip() + '/' + backup_file_name)

# grab settings and options
option_json = db.db_option_status_read()['mm_options_json']
if option_json['Backup']['BackupType'] != 'local':
    common_cloud.com_cloud_file_store(option_json['Backup']['BackupType'],\
    config_handle.get('MediaKrakenServer', 'BackupLocal').strip() + '/'\
    + backup_file_name, backup_file_name, True)

# log end
db.db_activity_insert('MediaKraken_Server Postgresql Backup Stop', None,\
    'System: Server DB Backup Stop', 'ServerBackupStop', None, None, 'System')

# commit records
db.db_commit()

# close the database
db.db_close()
