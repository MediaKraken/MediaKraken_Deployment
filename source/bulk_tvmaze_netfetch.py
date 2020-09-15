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
import uuid

from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_metadata_tvmaze

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START',
                                                     index_name='bulk_tvmaze_netfetch')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# setup the tvmaze class
if option_config_json['API']['tvmaze'] is not None:
    TVMAZE_CONNECTION = common_metadata_tvmaze.CommonMetadatatvmaze()
    for page_ndx in range(1, 1000):
        result = TVMAZE_CONNECTION.com_meta_tvmaze_show_list(page_ndx)
        show_list_json = json.loads(result)
        if len(show_list_json) == 0:
            break
        for show_ndx in range(0, len(show_list_json)):
            tvmaze_id = show_list_json[show_ndx]['id']
            # check to see if already downloaded
            if db_connection.db_metatv_guid_by_tvmaze(str(tvmaze_id)) is None:
                if db_connection.db_download_que_exists(None, common_global.DLMediaType.TV.value,
                                                        'tvmaze', str(tvmaze_id)) is None:
                    db_connection.db_download_insert('tvmaze', common_global.DLMediaType.TV.value,
                                                     json.dumps({"Status": "Fetch",
                                                                 "ProviderMetaID": str(
                                                                     tvmaze_id),
                                                                 "MetaNewID": str(
                                                                     uuid.uuid4())}))
        # commit all changes
        db_connection.db_commit()

common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='STOP')
