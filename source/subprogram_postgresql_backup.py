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

import os
import time

from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_network_cloud
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'subprogram_postgresql_backup')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# generate dump file
backup_file_name = 'MediaKraken_Database_Backup_' + \
                   time.strftime("%Y%m%d%H%M%S") + '.dump'

os.system('PGPASSWORD=' + os.environ['POSTGRES_PASSWORD']
          + ' pg_dump -h mkdatabase -U ' + os.environ['POSTGRES_USER'] + ' '
          + os.environ['POSTGRES_DB'] + ' -F c -f '
          + os.path.join('/mediakraken/backup', backup_file_name))

if option_config_json['Backup']['BackupType'] != 'local':
    cloud_handle = common_network_cloud.CommonLibCloud(option_config_json)
    cloud_handle.com_net_cloud_upload(
        container_name=option_config_json['MediaKrakenServer']['BackupContainerName'],
        input_file_name=os.path.join(
            option_config_json['MediaKrakenServer']['BackupLocal'], backup_file_name),
        output_file_name=backup_file_name)

# commit records
db_connection.db_commit()

# close the database
db_connection.db_close()
