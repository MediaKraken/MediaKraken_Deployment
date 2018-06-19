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
from common import common_global
from common import common_logging_elasticsearch

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'subprogram_roku_thumb_generate')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# go through ALL known media files
thumbnails_generated = 0
for row_data in db_connection.db_known_media():
    # TODO  actually, this should probably be the metadata
    # TODO the common roku code has the bif/thumb gen
    common_global.es_inst.com_elastic_index('info', {'row': row_data})

# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
