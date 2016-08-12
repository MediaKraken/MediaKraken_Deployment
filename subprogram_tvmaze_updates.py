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
sys.path.append("../MediaKraken_Common")
sys.path.append("../MediaKraken_Server")
import common_file
import common_logging
import common_Metadata_TVMaze
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

# create the file for pid
pid_file = '../pid/' + str(os.getpid())
common_file.common_file_Save_Data(pid_file, 'TVMaze Update', False, False, None)


def signal_receive(signum, frame):
    print('CHILD TVMaze Update: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_Rollback()
    db.srv_db_Close()
    sys.stdout.flush()
    sys.exit(0)


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
common_logging.common_logging_Start('./log/MediaKraken_Subprogram_TVMaze_Updates')


# open the database
db = database_base.MK_Server_Database()
db.srv_db_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_Activity_Insert('MediaKraken_Server TVMaze Update Start', None,\
    'System: Server TVMaze Start', 'ServertheTVMazeStart', None, None, 'System')


# grab the show data and update/insert respecitivey
def update_insert_show(tvmaze_id, update_rec=None):
    #show_full_json = TVMaze.com_Metadata_TheMaze_Show_By_ID(tvmaze_id, None, None, None, True)
    show_full_json = None
    try:
        show_full_json = ({'Meta': {'TVMaze': json.loads(TVMaze.com_Metadata_TheMaze_Show_By_ID(tvmaze_id, None, None, None, True))}})
    except:
        pass
    logging.debug("full: %s", show_full_json)
    if show_full_json is not None:
#        for show_detail in show_full_json:
        show_detail = show_full_json['Meta']['TVMaze']
        logging.debug("detail: %s", show_detail)
        tvmaze_name = show_detail['name']
        logging.debug("name: %s", tvmaze_name)
        try:
            tvrage_id = str(show_detail['externals']['tvrage'])
        except:
            tvrage_id = None
        try:
            thetvdb_id = str(show_detail['externals']['thetvdb'])
        except:
            thetvdb_id = None
        try:
            imdb_id = str(show_detail['externals']['imdb'])
        except:
            imdb_id = None
        series_id_json = json.dumps({'TVMaze':str(tvmaze_id), 'TVRage':tvrage_id,\
            'IMDB':imdb_id, 'theTVDB':thetvdb_id})
        if update_rec is None:
            image_json = {'Images': {'TVMaze': {'Characters': {}, 'Episodes': {}, "Redo": True}}}
            db.srv_db_MetadataTVMaze_Insert(series_id_json, tvmaze_name,\
                json.dumps(show_full_json), json.dumps(image_json))
        else:
            db.srv_db_MetadataTVMaze_Update(series_id_json, tvmaze_name,\
                json.dumps(show_full_json), json.dumps(image_json), str(tvmaze_id))
        # store person info
        if 'cast' in show_full_json['Meta']['TVMaze']['_embedded']:
            db.srv_db_Metadata_Person_Insert_Cast_Crew('TVMaze',\
                show_full_json['Meta']['TVMaze']['_embedded']['cast'])
        if 'crew' in show_full_json['Meta']['TVMaze']['_embedded']:
            db.srv_db_Metadata_Person_Insert_Cast_Crew('TVMaze',\
                show_full_json['Meta']['TVMaze']['_embedded']['crew'])
        db.srv_db_Commit()


# grab updated show list with epoc data
tvshow_updated = 0
tvshow_inserted = 0
TVMaze = com_Metadata_TVMaze.com_Metadata_TVMaze_API()
result = TVMaze.com_Metadata_TheMaze_Show_Updated()
#for show_list_json in result:
result = json.loads(result)
for tvmaze_id, tvmaze_time in result.items():
    logging.debug("id: %s", tvmaze_id)
    # check to see if allready downloaded
    results = db.srv_db_MetadataTV_GUID_By_TVMaze(str(tvmaze_id))
    if results is not None:
        # if show was updated since db record
        # TODO if results['updated'] < tvmaze_time:
        #update_insert_show(tvmaze_id, results[0]) # update the guid
        logging.debug("update")
        tvshow_updated += 1
    else:
        # insert new record as it's a new show
        update_insert_show(tvmaze_id, None)
        tvshow_inserted += 1


# log end
db.srv_db_Activity_Insert('MediaKraken_Server TVMaze Update Stop', None,\
    'System: Server TVMaze Stop', 'ServertheTVMazeStop', None, None, 'System')


# send notications
if tvshow_updated > 0:
    db.srv_db_Notification_Insert(locale.format('%d', tvshow_updated, True)\
        + " TV show(s) metadata updated.", True)
if tvshow_inserted > 0:
    db.srv_db_Notification_Insert(locale.format('%d', tvshow_inserted, True)\
        + " TV show(s) metadata added.", True)


# commit all changes to db
db.srv_db_Commit()


# close DB
db.srv_db_Close()


# remove pid
os.remove(pid_file)
