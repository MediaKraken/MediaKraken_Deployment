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
import logging
import ConfigParser
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
import sys
import json
import signal
import os
sys.path.append("./common")
sys.path.append("./server")
from common import common_file
from common import common_logging
from common import common_metadata
from common import common_network
from common import common_metadata_tmdb
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Sub_Collection', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Collections: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_rollback()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Update_Create_Collections')

# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
    config_handle.get('DB Connections', 'PostDBPort').strip(),\
    config_handle.get('DB Connections', 'PostDBName').strip(),\
    config_handle.get('DB Connections', 'PostDBUser').strip(),\
    config_handle.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_activity_insert('MediaKraken_Server Create Collection Start', None,\
    'System: Server Create Collection Start', 'ServerCreateCollectionStart', None, None, 'System')

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# verify themovietb key exists
if config_handle.get('API', 'themoviedb').strip() != 'None':
    # setup the thmdb class
    TMDB_API_Connection = common_metadata_tmdb.CommonMetadataTMDB()
else:
    TMDB_API_Connection = None
    logging.critical("themoviedb API not available. Exiting program...")
    sys.exit(0)


total_collections_downloaded = 0
# same code in subprogram match anime scudlee
def store_update_record(db_connection, collection_name, guid_list, poster_path, backdrop_path, collection_id):
    global total_collections_downloaded
    # store/update the record
    collection_guid = db.srv_db_collection_by_tmdb(collection_id) # don't string this since it's a pure result store
    logging.debug("colfsdfsd: %s %s", collection_id, collection_guid)
    if collection_guid is None:
        # insert
        collection_meta = TMDB_API_Connection.com_tmdb_metadata_collection_by_id(collection_id)
        logging.debug("col: %s", collection_meta)
        # poster path
        if poster_path is not None:
            image_poster_path = com_metadata.com_metadata_image_path(collection_name,\
                'poster', 'tmdb', poster_path)
        else:
            image_poster_path = ''
        # backdrop path
        if backdrop_path is not None:
            image_backdrop_path = com_metadata.com_metadata_image_path(collection_name,\
                'backdrop', 'tmdb', backdrop_path)
        else:
            image_backdrop_path = ''
        localimage_json = {'Poster': image_poster_path, 'Backdrop': image_backdrop_path}
        db.srv_db_collection_insert(collection_name, guid_list,\
            collection_meta, localimage_json)
        # commit all changes to db
        db.srv_db_commit()
        total_collections_downloaded += 1
    else:
        # update
        #db.srv_db_collection_update(collection_guid, guid_list)
        pass


# pull in all metadata with part of collection in metadata
old_collection_name = ''
old_poster_path = None
old_backdrop_path = None
old_id= None
guid_list = []
first_record = True
for row_data in db.srv_db_media_collection_scan():
    #mm_metadata_collection_name jsonb, mm_metadata_collection_media_ids
    if old_collection_name != row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['name']:
        if not first_record:
            store_update_record(db_connection, old_collection_name, guid_list, old_poster_path, old_backdrop_path, old_id)
        old_collection_name = row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['name']
        old_poster_path = row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['poster_path']
        old_backdrop_path = row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['backdrop_path']
        old_id = row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['id']
        guid_list = []
        first_record = False
    guid_list.append(row_data['mm_metadata_guid'])
# do last insert/update
if len(guid_list) > 0:
    store_update_record(db_connection, old_collection_name, guid_list, old_poster_path,\
        old_backdrop_path, old_id)


if total_collections_downloaded > 0:
    db.srv_db_notification_insert(locale.format('%d',\
        total_collections_downloaded, True) + " collection(s) metadata downloaded.", True)


# log end
db.srv_db_activity_insert('MediaKraken_Server Create Collection Stop', None,\
    'System: Server Create Collection Stop', 'ServerCreateCollectionStop', None, None, 'System')

# commit all changes to db
db.srv_db_commit()

# close the database
db.srv_db_close()

# remove pid
os.remove(pid_file)
