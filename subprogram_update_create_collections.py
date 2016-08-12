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
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import sys
import json
import signal
import os
sys.path.append("../common")
sys.path.append("../server")
import common_file
import common_logging
import common_Metadata
import common_network
import common_metadata_tmdb
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

# create the file for pid
pid_file = '../pid/' + str(os.getpid())
common_file.common_file_Save_Data(pid_file, 'Sub_Collection', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Collections: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_Rollback()
    db.srv_db_Close()
    sys.stdout.flush()
    sys.exit(0)

# start logging
common_logging.common_logging_Start('./log/MediaKraken_Subprogram_Update_Create_Collections')

# open the database
db = database_base.MK_Server_Database()
db.srv_db_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_Activity_Insert('MediaKraken_Server Create Collection Start', None,\
    'System: Server Create Collection Start', 'ServerCreateCollectionStart', None, None, 'System')

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# verify themovietb key exists
if Config.get('API', 'theMovieDB').strip() != 'None':
    # setup the thmdb class
    TMDB_API_Connection = common_metadata_tmdb.common_metadata_tmdb_API()
else:
    TMDB_API_Connection = None
    logging.critical("theMovieDB API not available. Exiting program...")
    sys.exit(0)


total_collections_downloaded = 0
# same code in subprogram match anime scudlee
def store_update_record(db, collection_name, guid_list, poster_path, backdrop_path, collection_id):
    global total_collections_downloaded
    # store/update the record
    collection_guid = db.srv_db_Collection_By_TMDB(collection_id) # don't string this since it's a pure result store
    logging.debug("colfsdfsd: %s %s", collection_id, collection_guid)
    if collection_guid is None:
        # insert
        collection_meta = TMDB_API_Connection.com_TMDB_Metadata_Collection_By_ID(collection_id)
        logging.debug("col: %s", collection_meta)
        # poster path
        if poster_path is not None:
            image_poster_path = com_Metadata.com_MetaData_Image_Path(collection_name,\
                'poster', 'tmdb', poster_path)
        else:
            image_poster_path = ''
        # backdrop path
        if backdrop_path is not None:
            image_backdrop_path = com_Metadata.com_MetaData_Image_Path(collection_name,\
                'backdrop', 'tmdb', backdrop_path)
        else:
            image_backdrop_path = ''
        localimage_json = {'Poster': image_poster_path, 'Backdrop': image_backdrop_path}
        db.srv_db_Collection_Insert(collection_name, guid_list,\
            collection_meta, localimage_json)
        # commit all changes to db
        db.srv_db_Commit()
        total_collections_downloaded += 1
    else:
        # update
        #db.srv_db_Collection_Update(collection_guid, guid_list)
        pass


# pull in all metadata with part of collection in metadata
old_collection_name = ''
old_poster_path = None
old_backdrop_path = None
old_id= None
guid_list = []
first_record = True
for row_data in db.srv_db_Media_Collection_Scan():
    #mm_metadata_collection_name jsonb, mm_metadata_collection_media_ids
    if old_collection_name != row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['name']:
        if not first_record:
            store_update_record(db, old_collection_name, guid_list, old_poster_path, old_backdrop_path, old_id)
        old_collection_name = row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['name']
        old_poster_path = row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['poster_path']
        old_backdrop_path = row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['backdrop_path']
        old_id = row_data['mm_metadata_json']['Meta']['TMDB']['Meta']['belongs_to_collection']['id']
        guid_list = []
        first_record = False
    guid_list.append(row_data['mm_metadata_guid'])
# do last insert/update
if len(guid_list) > 0:
    store_update_record(db, old_collection_name, guid_list, old_poster_path,\
        old_backdrop_path, old_id)


if total_collections_downloaded > 0:
    db.srv_db_Notification_Insert(locale.format('%d',\
        total_collections_downloaded, True) + " collection(s) metadata downloaded.", True)


# log end
db.srv_db_Activity_Insert('MediaKraken_Server Create Collection Stop', None,\
    'System: Server Create Collection Stop', 'ServerCreateCollectionStop', None, None, 'System')

# commit all changes to db
db.srv_db_Commit()

# close the database
db.srv_db_Close()

# remove pid
os.remove(pid_file)
