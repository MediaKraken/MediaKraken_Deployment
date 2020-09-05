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

from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch

dont_force_localhost = True

if dont_force_localhost:
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('db_update_version')
    # open the database
    option_config_json, db_connection = common_config_ini.com_config_read()
else:
    # open the database
    option_config_json, db_connection = common_config_ini.com_config_read(force_local=True)

# read in all mm_metadata_movie where mm_metadata_localimage_json is not null
for metadata_movie_record in db_connection.db_query('select mm_metadata_media_id,'
                                                    ' mm_metadata_localimage_json'
                                                    ' from mm_metadata_movie'
                                                    ' where mm_metadata_localimage_json'
                                                    ' is not null'):
    print('Movie Record: ', metadata_movie_record, flush=True)

for metadata_tv_record in db_connection.db_query('select mm_metadata_media_tvshow_id,'
                                                 ' mm_metadata_tvshow_localimage_json'
                                                 ' from mm_metadata_tvshow'
                                                 ' where mm_metadata_tvshow_localimage_json'
                                                 ' is not null'):
    print('TV Record: ', metadata_tv_record, flush=True)

for metadata_person_record in db_connection.db_query('select mmp_id_pk,'
                                                     ' mmp_person_image'
                                                     ' from mm_metadata_person'
                                                     ' where mmp_person_image'
                                                     ' is not null'):
    print('Person Record: ', metadata_person_record, flush=True)

# close the database
db_connection.db_close()
