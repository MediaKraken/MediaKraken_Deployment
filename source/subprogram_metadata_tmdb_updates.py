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

import json
import uuid

from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_metadata_tmdb
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_tmdb_updates')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# grab the updated data
tmdb = common_metadata_tmdb.CommonMetadataTMDB(option_config_json)

# TODO this should go thru the limiter
# process movie changes
for movie_change in tmdb.com_tmdb_meta_changes_movie()['results']:
    common_global.es_inst.com_elastic_index('info', {'mov': movie_change['id']})
    if db_connection.db_meta_guid_by_tmdb(str(movie_change['id'])) is None:
        common_global.es_inst.com_elastic_index('info', {'here': '1'})
        dl_meta = db_connection.db_download_que_exists(None, 1, 'themoviedb',
                                                       str(movie_change['id']))
        common_global.es_inst.com_elastic_index('info', {'dl_meta': dl_meta})
        if dl_meta is None:
            db_connection.db_download_insert('themoviedb', 1, json.dumps({'MediaID': None,
                                                                          'Path': None,
                                                                          'ClassID': None,
                                                                          'Status': 'Fetch',
                                                                          'MetaNewID': str(
                                                                              uuid.uuid4()),
                                                                          'ProviderMetaID': str(
                                                                              movie_change['id'])}))
    else:
        db_connection.db_download_insert('themoviedb', 1, json.dumps({'MediaID': None,
                                                                      'Path': None, 'ClassID': None,
                                                                      'Status': 'Update',
                                                                      'MetaNewID': str(
                                                                          uuid.uuid4()),
                                                                      'ProviderMetaID': str(
                                                                          movie_change['id'])}))

# process tv changes
# for tv_change in tmdb.com_tmdb_meta_changes_tv()['results']:
#     common_global.es_inst.com_elastic_index('info', {'stuff':"tv: %s", tv_change['id'])
#     if db_connection.db_metatv_guid_by_tmdb(str(tv_change['id'])) is None:
#         dl_meta = db_connection.db_download_que_exists(None, 'themoviedb', str(tv_change['id']))
#         if dl_meta is None:
#             status_type = 'Fetch'
#     else:
#         db_connection.db_download_insert('themoviedb', json.dumps({'MediaID': None,
#             'Path': None, 'ClassID': None, 'Status': 'Update',
#             'MetaNewID': str(uuid.uuid4()), 'ProviderMetaID': str(tv_change['id'])}))

# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
