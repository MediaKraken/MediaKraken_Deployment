"""
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
  Software Foundation, Inc., 51 Franklin Street,
  Fifth Floor, Boston,
  MA 02110-1301, USA.
"""

import json

from common import common_config_ini
from common import common_internationalization
from common import common_logging_elasticsearch_httpx
from common import common_signal

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# pull in all metadata with part of collection in metadata
old_collection_name = ''
old_poster_path = None
old_backdrop_path = None
old_id = None
guid_list = []
first_record = True
total_collections_downloaded = 0
for row_data in db_connection.db_media_collection_scan():
    # mm_metadata_collection_name jsonb, mm_metadata_collection_media_ids
    if old_collection_name != \
            row_data['mm_metadata_json']['belongs_to_collection'][
                'name']:
        if not first_record:
            db_connection.db_download_insert('themoviedb',
                                             json.dumps({'Status': 'FetchCollection',
                                                         'Name': old_collection_name,
                                                         'GUID': guid_list,
                                                         'Poster': old_poster_path,
                                                         'Backdrop': old_backdrop_path,
                                                         'ProviderMetaID': str(old_id)}))
            total_collections_downloaded += 1
        old_collection_name = \
            row_data['mm_metadata_json']['belongs_to_collection'][
                'name']
        old_poster_path = \
            row_data['mm_metadata_json']['belongs_to_collection'][
                'poster_path']
        old_backdrop_path = row_data['mm_metadata_json']['belongs_to_collection']['backdrop_path']
        old_id = \
            row_data['mm_metadata_json']['belongs_to_collection'][
                'id']
        guid_list = []
        first_record = False
    guid_list.append(row_data['mm_metadata_guid'])
# do last insert/update
if len(guid_list) > 0:
    db_connection.db_download_insert('themoviedb',
                                     json.dumps({'Status': 'FetchCollection',
                                                 'Name': old_collection_name,
                                                 'GUID': guid_list,
                                                 'Poster': old_poster_path,
                                                 'Backdrop': old_backdrop_path,
                                                 'ProviderMetaID': str(old_id)}))
    total_collections_downloaded += 1

if total_collections_downloaded > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(
            total_collections_downloaded)
        + " collection(s) metadata downloaded.", True)

# commit all changes to db
db_connection.db_commit()

# close the database
db_connection.db_close()
