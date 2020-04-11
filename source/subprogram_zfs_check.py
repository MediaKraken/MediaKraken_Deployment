"""
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
"""

from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_network_ssh
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_zfs_check')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# loop through zfs host list and validate
for zfs_host in option_config_json['zfs']['host']:
    ssh_instance = common_network_ssh.CommonNetworkSSH(zfs_host['host'],
                                                       zfs_host['user_name'],
                                                       zfs_host['user_password'])
    zfs_status = ssh_instance.com_net_ssh_run_command(
        'zpool list -H -o health')
    # TODO check zfs_status for string to determine bad pool
    # TODO and send notification
    ssh_instance.com_net_ssh_close()

# commit all changes
db_connection.db_commit()

# close the database
db_connection.db_close()
