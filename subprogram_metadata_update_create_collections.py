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
  Software Foundation, Inc., 51 Franklin Street,
  Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import sys
import json
from common import common_config_ini
from common import common_logging
from common import common_metadata_tmdb
from common import common_signal
import locale
locale.setlocale(locale.LC_ALL, '')


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Update_Create_Collections')


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Create Collection Start', None,\
    'System: Server Create Collection Start', 'ServerCreateCollectionStart', None, None, 'System')


# verify themovietb key exists
if option_config_json['API']['themoviedb'] is not None:
    # setup the thmdb class
    TMDB_API_CONNECTION = common_metadata_tmdb.CommonMetadataTMDB(option_config_json)
else:
    TMDB_API_CONNECTION = None
    logging.critical("themoviedb API not available. Exiting program...")
    sys.exit(0)


# pull in all metadata with part of collection in metadata
old_collection_name = ''
old_poster_path = None
old_backdrop_path = None
old_id = None
guid_list = []
first_record = True
total_collections_downloaded = 0
for row_data in db_connection.db_media_collection_scan():
    #mm_metadata_collection_name jsonb, mm_metadata_collection_media_ids
    if old_collection_name != row_data['mm_metadata_json']['Meta']\
            ['themoviedb']['Meta']['belongs_to_collection']['name']:
        if not first_record:
            db_connection.db_download_insert('themoviedb',\
                json.dumps({'Status': 'FetchCollection',\
                'Name': old_collection_name, 'GUID': guid_list,\
                'Poster': old_poster_path, 'Backdrop': old_backdrop_path,\
                'ProviderMetaID': str(old_id)}))
            total_collections_downloaded += 1
        old_collection_name = row_data['mm_metadata_json']['Meta']\
            ['themoviedb']['Meta']['belongs_to_collection']['name']
        old_poster_path = row_data['mm_metadata_json']['Meta']\
            ['themoviedb']['Meta']['belongs_to_collection']['poster_path']
        old_backdrop_path = row_data['mm_metadata_json']['Meta']\
            ['themoviedb']['Meta']['belongs_to_collection']['backdrop_path']
        old_id = row_data['mm_metadata_json']['Meta']\
            ['themoviedb']['Meta']['belongs_to_collection']['id']
        guid_list = []
        first_record = False
    guid_list.append(row_data['mm_metadata_guid'])
# do last insert/update
if len(guid_list) > 0:
    db_connection.db_download_insert('themoviedb',\
        json.dumps({'Status': 'FetchCollection',\
        'Name': old_collection_name, 'GUID': guid_list,\
        'Poster': old_poster_path, 'Backdrop': old_backdrop_path,\
        'ProviderMetaID': str(old_id)}))
    total_collections_downloaded += 1


if total_collections_downloaded > 0:
    db_connection.db_notification_insert(locale.format('%d',\
        total_collections_downloaded, True) + " collection(s) metadata downloaded.", True)


# log end
db_connection.db_activity_insert('MediaKraken_Server Create Collection Stop', None,\
    'System: Server Create Collection Stop', 'ServerCreateCollectionStop', None, None, 'System')


# commit all changes to db
db_connection.db_commit()


# vaccum tables that had records added
db_connection.db_pgsql_vacuum_table('mm_metadata_collection')


# close the database
db_connection.db_close()
