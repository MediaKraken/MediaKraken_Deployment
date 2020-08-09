"""
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
"""

import json
import sys

from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch
from common import common_metadata_provider_anidb
from common import common_metadata_scudlee
from common import common_signal
from common import common_system

# verify this program isn't already running!
if common_system.com_process_list(
        process_name='/usr/bin/python3 /mediakraken/subprogram_metadata_anidb_updates.py'):
    sys.exit(0)

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_metadata_anidb_updates')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# TODO this should go through the limiter
# stage totals
anime_added = 0
# grab the updated data
anidb = common_metadata_provider_anidb.CommonMetadataANIdb(db_connection)
anidb.com_net_anidb_fetch_titles_file()
# insert into db
anidb.com_net_anidb_save_title_data_to_db()
# grab latest scudlee udpate
common_metadata_scudlee.mk_scudlee_fetch_xml()

# store the xref data
for anidbid, tvdbid, imdbid, default_tvseason, mapping_data, before_data \
        in common_metadata_scudlee.mk_scudlee_anime_list_parse():
    common_global.es_inst.com_elastic_index('info', {
        'stuff': {'ani': anidbid,
                  ' tv': tvdbid,
                  ' imdb': imdbid,
                  ' default': default_tvseason,
                  ' map': mapping_data,
                  ' before': before_data}})
    db_connection.db_meta_anime_update_meta_id(json.dumps({'anidb': anidbid,
                                                           'thetvdb': tvdbid, 'imdb': imdbid}),
                                               json.dumps({'Default': default_tvseason,
                                                           'Map': mapping_data}), before_data)

# store the xref collection data
for scud_collection in common_metadata_scudlee.mk_scudlee_anime_set_parse():
    pass

# send notifications
if anime_added > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(anime_added)
        + " Anime metadata updated.", True)
    create_collection_trigger = True

# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
