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

from common import common_config_ini
from common import common_file
from common import common_global
from common import common_logging_elasticsearch
from common import common_network_radio
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_iradio')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# # start code for updating iradio database
# common_network_radio.com_net_radio()
#
# # load the cache files and compare to db
# radio_cache = common_file.com_file_load_data('./cache.pickle', True)
# for row_data in radio_cache:
#     common_global.es_inst.com_elastic_index('info', {'radio cache': row_data})
#     db_connection.db_iradio_insert(row_data)
#
# # radio_xiph = common_file.com_file_load_data('./xiph.pickle', True)


# commit
db_connection.db_commit()

# vaccum tables that had records added
db_connection.db_pgsql_vacuum_table('mm_radio')

# close the database
db_connection.db_close()
