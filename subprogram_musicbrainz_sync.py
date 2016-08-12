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
sys.path.append("../common")
sys.path.append("../server")
import common_file
import common_logging
import database as database_base
import db_base_brainz as database_base_brainz

# create the file for pid
pid_file = '../pid/' + str(os.getpid())
common_file.common_file_Save_Data(pid_file, 'Musicbrainz_Sync', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Mbrainz Sync: Received USR1')
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
common_logging.common_logging_Start('./log/MediaKraken_Subprogram_MusicBrainz_Sync')


# open the database
db = database_base.MK_Server_Database()
db.srv_db_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


# open the remote musicbrainz db
db_brainz = database_base_brainz.srv_db_Brainz()
db_brainz.srv_db_Open(Config.get('MediaBrainz', 'BrainzDBHost').strip(),\
    Config.get('MediaBrainz', 'BrainzDBPort').strip(),\
    Config.get('MediaBrainz', 'BrainzDBName').strip(),\
    Config.get('MediaBrainz', 'BrainzDBUser').strip(),\
    Config.get('MediaBrainz', 'BrainzDBPass').strip())

# log start
db.srv_db_Activity_Insert('MediaKraken_Server MusicBrainz Start', None,\
    'System: Server MusicBrainz Start', 'ServerMusicBrainzStart', None, None, 'System')

# fetch all the artists from brainz
for row_data in db_brainz.srv_db_Brainz_All_Artists():
    db.srv_db_Metadata_Musician_Add(row_data['name'],\
        json.dumps({'MusicBrainz':row_data['gid']}), json.dumps({'Comment':row_data['comment'],\
        'Gender':row_data['gender'], 'Begin':(str(row_data['begin_date_year']) + ':'\
        + str(row_data['begin_date_month']) + ':' + str(row_data['begin_date_day'])),\
        'End':(str(row_data['end_date_year']) + ':' + str(row_data['end_date_month']) + ':'\
        + str(row_data['end_date_day']))}))
    logging.debug(row_data)
    # fetch all the albums from brainz by artist
    for row_data_album in db_brainz.srv_db_Brainz_All_Albums_By_Artist(row_data['id']):
        db.srv_db_Metadata_Album_Add(row_data_album['name'],\
            json.dumps({'MusicBrainz':row_data_album['gid']}),\
            json.dumps({'Commment':row_data_album['comment'],\
            'Language':row_data_album['language'], 'Barcode':row_data_album['barcode']}))
        logging.debug(row_data_album)
'''
        # fetch all the songs from brainz
        for row_data in db_brainz.srv_db_Brainz_All_Songs():
            # 0 gid, 1 name, 2 recording, 3 position, 4 id
            db.srv_db_Metadata_Song_Add(row_data[99],json.dumps({ 'MusicBrainz':row_data[0] }),json.dumps({'':rowdata[99]}))
'''

# log end
db.srv_db_Activity_Insert('MediaKraken_Server MusicBrainz Stop', None,\
    'System: Server MusicBrainz Stop', 'ServerMusicBrainzStop', None, None, 'System')

# commit all changes to db
db.srv_db_Commit()
# close DB
db_brainz.srv_db_Close()
db.srv_db_Close()
# remove pid
os.remove(pid_file)
