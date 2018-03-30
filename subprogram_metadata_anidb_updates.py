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

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os

from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch
from common import common_metadata_anidb
from common import common_metadata_scudlee

# start logging
if os.environ['DEBUG']:
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_anidb_updates')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# stage totals
anime_added = 0
# grab the updated data
anidb = common_metadata_anidb.CommonMetadataANIdb(db_connection)
anidb.com_net_anidb_fetch_titles_file()
# insert into db
anidb.com_net_anidb_save_title_data_to_db()
# grab latest scudlee udpate
common_metadata_scudlee.mk_scudlee_fetch_xml()

# store the xref data
for anidbid, tvdbid, imdbid, default_tvseason, mapping_data, before_data \
        in common_metadata_scudlee.mk_scudlee_anime_list_parse():
    if os.environ['DEBUG']:
        common_global.es_inst.com_elastic_index('info', {
            'stuff': str(('ani %s, tv %s, imdb %s, default %s, map %s, before %s:', anidbid,
                          tvdbid, imdbid, default_tvseason, mapping_data, before_data))})
    db_connection.db_meta_anime_update_meta_id(json.dumps({'anidb': anidbid,
                                                           'thetvdb': tvdbid, 'imdb': imdbid}),
                                               json.dumps({'Default': default_tvseason,
                                                           'Map': mapping_data}), before_data)

# store the xref collection data
for scud_collection in common_metadata_scudlee.mk_scudlee_anime_set_parse():
    pass

# send notications
if anime_added > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(anime_added)
        + " Anime metadata updated.", True)
    create_collection_trigger = True

# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
