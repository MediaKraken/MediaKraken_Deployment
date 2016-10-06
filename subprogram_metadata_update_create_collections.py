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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import sys
from common import common_config_ini
from common import common_logging
from common import common_metadata
from common import common_metadata_tmdb
from common import common_signal
import locale
locale.setlocale(locale.LC_ALL, '')


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Update_Create_Collections')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Create Collection Start', None,\
    'System: Server Create Collection Start', 'ServerCreateCollectionStart', None, None, 'System')


# verify themovietb key exists
if option_config_json['API']['theMovieDB'] is not None:
    # setup the thmdb class
    TMDB_API_CONNECTION = common_metadata_tmdb.CommonMetadataTMDB(option_config_json)
else:
    TMDB_API_CONNECTION = None
    logging.critical("themoviedb API not available. Exiting program...")
    sys.exit(0)


# same code in subprogram match anime scudlee
def store_update_record(db_connection, collection_name, guid_list, poster_path,\
        backdrop_path, collection_id):
    # store/update the record
    # don't string this since it's a pure result store
    collection_guid = db_connection.db_collection_by_tmdb(collection_id)
    logging.debug("colfsdfsd: %s %s", collection_id, collection_guid)
    if collection_guid is None:
        # insert
        collection_meta = TMDB_API_CONNECTION.com_tmdb_meta_collection_by_id(collection_id)
        logging.debug("col: %s", collection_meta)
        # poster path
        if poster_path is not None:
            image_poster_path = common_metadata.com_meta_image_path(collection_name,\
                'poster', 'tmdb', poster_path)
        else:
            image_poster_path = None
        # backdrop path
        if backdrop_path is not None:
            image_backdrop_path = common_metadata.com_meta_image_path(collection_name,\
                'backdrop', 'tmdb', backdrop_path)
        else:
            image_backdrop_path = None
        localimage_json = {'Poster': image_poster_path, 'Backdrop': image_backdrop_path}
        db_connection.db_collection_insert(collection_name, guid_list,\
            collection_meta, localimage_json)
        # commit all changes to db
        db_connection.db_commit()
        return 1 # to add totals later
    else:
        # update
        #db_connection.db_collection_update(collection_guid, guid_list)
        return 0 # to add totals later


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
            ['TMDB']['Meta']['belongs_to_collection']['name']:
        if not first_record:
            total_collections_downloaded += store_update_record(db_connection,\
                old_collection_name, guid_list,\
                old_poster_path, old_backdrop_path, old_id)
        old_collection_name = row_data['mm_metadata_json']['Meta']\
            ['TMDB']['Meta']['belongs_to_collection']['name']
        old_poster_path = row_data['mm_metadata_json']['Meta']\
            ['TMDB']['Meta']['belongs_to_collection']['poster_path']
        old_backdrop_path = row_data['mm_metadata_json']['Meta']\
            ['TMDB']['Meta']['belongs_to_collection']['backdrop_path']
        old_id = row_data['mm_metadata_json']['Meta']\
            ['TMDB']['Meta']['belongs_to_collection']['id']
        guid_list = []
        first_record = False
    guid_list.append(row_data['mm_metadata_guid'])
# do last insert/update
if len(guid_list) > 0:
    total_collections_downloaded += store_update_record(db_connection,\
        old_collection_name, guid_list, old_poster_path,\
        old_backdrop_path, old_id)


if total_collections_downloaded > 0:
    db_connection.db_notification_insert(locale.format('%d',\
        total_collections_downloaded, True) + " collection(s) metadata downloaded.", True)


# log end
db_connection.db_activity_insert('MediaKraken_Server Create Collection Stop', None,\
    'System: Server Create Collection Stop', 'ServerCreateCollectionStop', None, None, 'System')

# commit all changes to db
db_connection.db_commit()

# close the database
db_connection.db_close()
