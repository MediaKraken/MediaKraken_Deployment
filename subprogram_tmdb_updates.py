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
import logging
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import sys
import os
import signal
import json
import uuid
sys.path.append("../MediaKraken_Common")
sys.path.append("../MediaKraken_Server")
import MK_Common_File
import MK_Common_Logging
import MK_Common_Metadata_TMDB
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

# create the file for pid
pid_file = '../pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'TMDB Update', False, False, None)

def signal_receive(signum, frame):
    print('CHILD TMDB Update: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_TMDB_Updates')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.MK_Server_Database_Activity_Insert('MediaKraken_Server TMDB Update Start', None,\
    'System: Server TMDB Start', 'ServertheTMDBStart', None, None, 'System')


# grab the data
tvshow_updated = 0
tvshow_inserted = 0
movie_updated = 0
movie_inserted = 0


# fetch from tmdb
def movie_fetch_save(tmdb_id):
    metadata_uuid = None
    logging.debug("fetch: %s", tmdb_id)
    # fetch and save json data via tmdb id
    result_json = tmdb.MK_Common_TMDB_Metadata_By_ID(tmdb_id)
    if result_json is not None:
        logging.debug("here I am")
        series_id_json, result_json, image_json = tmdb.MK_Common_TMDB_MetaData_Info_Build(result_json)
        cast_json = tmdb.MK_Common_TMDB_Metadata_Cast_By_ID(tmdb_id)
        # set and insert the record
        meta_json = ({'Meta': {'TMDB': {'Meta': result_json, 'Cast': cast_json['cast'], 'Crew': cast_json['crew']}}})
        # check for previous record
        if db.MK_Server_Database_Metadata_TMDB_Count(result_json['id']) > 0:
            # TODO if this is > 0......MUST use series id from DB.......so, stuff doesn't get wiped
            #db.MK_Server_Database_Metadata_Update(series_id_json, result_json['title'], json.dumps(meta_json), json.dumps(image_json))
            pass
        else:
            # store person info
            if 'cast' in cast_json:
                db.MK_Server_Database_Metadata_Person_Insert_Cast_Crew('TMDB', cast_json['cast'])
            if 'crew' in cast_json:
                db.MK_Server_Database_Metadata_Person_Insert_Cast_Crew('TMDB', cast_json['crew'])
            # grab reviews
            review_json = tmdb.MK_Common_TMDB_Metadata_Review_By_ID(tmdb_id)
            if review_json['total_results'] > 0:
                review_json_id = ({'TMDB': str(review_json['id'])})
                logging.debug("review: %s", review_json_id)
                db.MK_Server_Database_Review_Insert(json.dumps(review_json_id), json.dumps({'TMDB': review_json}))
            # set and insert the record
            metadata_uuid = str(uuid.uuid4())
            db.MK_Server_Database_Metadata_Insert_TMDB(metadata_uuid, series_id_json, result_json['title'], json.dumps(meta_json), json.dumps(image_json))
    return metadata_uuid


# grab the updated data
tmdb = MK_Common_TMDB.MK_Common_Metadata_TMDB_API()
for movie_change in tmdb.MK_Common_TMDB_Metadata_Changes_Movie()['results']:
    logging.debug("mov: %s", movie_change['id'])
    movie_fetch_save(movie_change['id'])
for tv_change in tmdb.MK_Common_TMDB_Metadata_Changes_TV()['results']:
    logging.debug("tv: %s", tv_change['id'])
    movie_fetch_save(tv_change['id'])


# log end
db.MK_Server_Database_Activity_Insert('MediaKraken_Server TMDB Update Stop', None,\
    'System: Server TMDB Stop', 'ServertheTMDBStop', None, None, 'System')


create_collection_trigger = False
# send notications
if tvshow_updated > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', tvshow_updated, True) + " TV show(s) metadata updated.", True)
    create_collection_trigger = True
if tvshow_inserted > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', tvshow_inserted, True) + " TV show(s) metadata added.", True)
    create_collection_trigger = True
if movie_updated > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', movie_updated, True) + " movie metadata updated.", True)
    create_collection_trigger = True
if movie_inserted > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', movie_inserted, True) + " movie metadata added.", True)
    create_collection_trigger = True
# update collection
if create_collection_trigger:
    db.MK_Server_Database_Trigger_Insert(('python', './subprogram/metadata/subprogram_update_create_collections.py'))


# commit all changes
db.MK_Server_Database_Commit()


# close DB
db.MK_Server_Database_Close()


# remove pid
os.remove(pid_file)
