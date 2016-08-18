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
import ConfigParser
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
import sys
import signal
import os
from common import common_file
from common import common_logging
from common import common_metadata_scudlee
import database as database_base

# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Sub_Anime_Match', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Anime: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.db_rollback()
    db.db_close()
    sys.stdout.flush()
    sys.exit(0)

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Anime_Scudlee')

# open the database
db = database_base.MKServerDatabase()
db.db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
    config_handle.get('DB Connections', 'PostDBPort').strip(),\
    config_handle.get('DB Connections', 'PostDBName').strip(),\
    config_handle.get('DB Connections', 'PostDBUser').strip(),\
    config_handle.get('DB Connections', 'PostDBPass').strip())


# log start
db.db_activity_insert('MediaKraken_Server Anime Scudlee Start', None,\
    'System: Server Anime Scudlee Start', 'ServerAnimeScudleeStart', None, None, 'System')

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c

# same code in subprograb update create collections
def store_update_record(db_connection, collection_name, guid_list):
    # store/update the record
    collection_guid = db.db_Collection_by_Name(collection_name)
    if collection_guid is None:
        # insert
        db.db_collection_insert(collection_name, guid_list)
    else:
        # update
        db.db_collection_update(collection_guid, guid_list)

# check for new scudlee download
com_scudlee.mk_scudlee_fetch_xml()
# begin the media match on NULL matches
for row_data in com_scudlee.mk_scudlee_anime_list_parse():
    logging.debug("row: %s", row_data)
    if row_data is not None:
        # skip media with "no" match...rowdata2 is imdbid
        if (row_data[1] == "OVA" or row_data[1] == "movie" or row_data[1] == "hentai"\
                or row_data[1] == "web") and row_data[2] is None:
            pass
        else:
            # should be valid data, do the update
            db.db_meta_update_media_id_from_scudlee(row_data[1],\
                row_data[2], row_data[0])

# begin the collections match/create/update
for row_data in com_scudlee.mk_scudlee_anime_set_parse():
    #db.db_meta_update_Collection_Media_ID_From_Scudlee(row_data[0],row_data[1])
    if row_data[1] == "music video":
        pass
    else:
        store_update_record(db_connection, row_data[0], row_data[1])

# log end
db.db_activity_insert('MediaKraken_Server Anime Scudlee Stop', None,\
    'System: Server Anime Scudlee Stop', 'ServerAnimeScudleeStop', None, None, 'System')
# commit all changes to db
db.db_commit()
# close the database
db.db_close()

# remove pid
os.remove(pid_file)
