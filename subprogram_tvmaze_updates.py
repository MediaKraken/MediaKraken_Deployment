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
import logging # pylint: disable=W0611
import ConfigParser
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
import sys
import os
import signal
import json
from common import common_file
from common import common_logging
from common import common_metadata_tvmaze
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'tvmaze Update', False, False, None)


def signal_receive(signum, frame):
    print('CHILD tvmaze Update: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_rollback()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_tvmaze_Updates')


# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
    config_handle.get('DB Connections', 'PostDBPort').strip(),\
    config_handle.get('DB Connections', 'PostDBName').strip(),\
    config_handle.get('DB Connections', 'PostDBUser').strip(),\
    config_handle.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_activity_insert('MediaKraken_Server tvmaze Update Start', None,\
    'System: Server tvmaze Start', 'ServerthetvmazeStart', None, None, 'System')


# grab the show data and update/insert respecitivey
def update_insert_show(tvmaze_id, update_rec=None):
    #show_full_json = tvmaze.com_meta_TheMaze_Show_by_ID(tvmaze_id, None, None, None, True)
    show_full_json = None
    try:
        show_full_json = ({'Meta': {'tvmaze': json.loads(tvmaze.com_meta_TheMaze_Show_by_ID(tvmaze_id, None, None, None, True))}})
    except:
        pass
    logging.debug("full: %s", show_full_json)
    if show_full_json is not None:
#        for show_detail in show_full_json:
        show_detail = show_full_json['Meta']['tvmaze']
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
        series_id_json = json.dumps({'tvmaze':str(tvmaze_id), 'TVRage':tvrage_id,\
            'imdb':imdb_id, 'thetvdb':thetvdb_id})
        if update_rec is None:
            image_json = {'Images': {'tvmaze': {'Characters': {}, 'Episodes': {}, "Redo": True}}}
            db.srv_db_metatvmaze_Insert(series_id_json, tvmaze_name,\
                json.dumps(show_full_json), json.dumps(image_json))
        else:
            db.srv_db_metatvmaze_Update(series_id_json, tvmaze_name,\
                json.dumps(show_full_json), json.dumps(image_json), str(tvmaze_id))
        # store person info
        if 'cast' in show_full_json['Meta']['tvmaze']['_embedded']:
            db.srv_db_meta_person_insert_cast_crew('tvmaze',\
                show_full_json['Meta']['tvmaze']['_embedded']['cast'])
        if 'crew' in show_full_json['Meta']['tvmaze']['_embedded']:
            db.srv_db_meta_person_insert_cast_crew('tvmaze',\
                show_full_json['Meta']['tvmaze']['_embedded']['crew'])
        db.srv_db_commit()


# grab updated show list with epoc data
tvshow_updated = 0
tvshow_inserted = 0
tvmaze = com_meta_tvmaze.com_meta_tvmaze_API()
result = tvmaze.com_meta_themaze_show_updated()
#for show_list_json in result:
result = json.loads(result)
for tvmaze_id, tvmaze_time in result.items():
    logging.debug("id: %s", tvmaze_id)
    # check to see if allready downloaded
    results = db.srv_db_metaTV_guid_by_tvmaze(str(tvmaze_id))
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
db.srv_db_activity_insert('MediaKraken_Server tvmaze Update Stop', None,\
    'System: Server tvmaze Stop', 'ServerthetvmazeStop', None, None, 'System')


# send notications
if tvshow_updated > 0:
    db.srv_db_notification_insert(locale.format('%d', tvshow_updated, True)\
        + " TV show(s) metadata updated.", True)
if tvshow_inserted > 0:
    db.srv_db_notification_insert(locale.format('%d', tvshow_inserted, True)\
        + " TV show(s) metadata added.", True)


# commit all changes to db
db.srv_db_commit()


# close DB
db.srv_db_close()


# remove pid
os.remove(pid_file)
