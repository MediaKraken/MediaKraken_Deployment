"""
  Copyright (C) 2020 Quinn D Granfor <spootdev@gmail.com>

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

from common import common_file
from common import common_network_pika
from common import common_watchdog

# scan initial directory for movie files
for file_name in common_file.com_file_dir_list('/home/spoot/nzbget/downloads/completed/Movies'):
    print(file_name, flush=True)
    common_network_pika.com_net_pika_send(body_data,
                                          rabbit_host_name='mkstack_rabbitmq',
                                          exchange_name='mkque_ex',
                                          route_key='mkque')

# scan initial directory for tv files
for file_name in common_file.com_file_dir_list('/home/spoot/nzbget/downloads/completed/Series'):
    print(file_name, flush=True)
    common_network_pika.com_net_pika_send(body_data,
                                          rabbit_host_name='mkstack_rabbitmq',
                                          exchange_name='mkque_ex',
                                          route_key='mkque')

# set watchdog for file directory
movie_file = common_watchdog.CommonWatchdog('/home/spoot/nzbget/downloads/completed/Movies')
series_file = common_watchdog.CommonWatchdog('/home/spoot/nzbget/downloads/completed/Series')
