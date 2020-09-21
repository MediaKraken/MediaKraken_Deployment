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
from common import common_metadata_provider_tvmaze
from common import common_signal

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START',
                                                     index_name='subprogram_metadata_tvmaze_udpates')

# set signal exit breaks
common_signal.com_signal_set_break()

# TODO this should go through the limiter
# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# grab updated show list with epoc data
tvmaze = common_metadata_provider_tvmaze.CommonMetadatatvmaze()
result = tvmaze.com_meta_tvmaze_show_updated()
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'result': result})
# for show_list_json in result:
result = json.loads(result)
for tvmaze_id, tvmaze_time in list(result.items()):
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={'id': tvmaze_id,
                                                                       'time': tvmaze_time})
    # check to see if already downloaded
    results = db_connection.db_metatv_guid_by_tvmaze(str(tvmaze_id))
    if results is not None:
        # if show was updated since db record
        # TODO if results['updated'] < tvmaze_time:
        # update_insert_show(tvmaze_id, results[0]) # update the guid
        pass
    else:
        if db_connection.db_download_que_exists(None, common_global.DLMediaType.TV.value, 'tvmaze',
                                                tvmaze_id) is None:
            # insert new record as it's a new show
            db_connection.db_download_insert(provider='tvmaze',
                                             que_type=common_global.DLMediaType.TV.value,
                                             down_json=json.dumps({'Status': 'Fetch',
                                                                   'ProviderMetaID': tvmaze_id}),
                                             down_new_uuid=uuid.uuid4(),
                                             )

# commit all changes to db
db_connection.db_commit()

# close DB
db_connection.db_close()
