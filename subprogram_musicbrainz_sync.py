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
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
import sys
import os
import signal
import json
sys.path.append("../common")
sys.path.append("../server")
from common import common_file
from common import common_logging
import database as database_base
import db_base_brainz as database_base_brainz

# create the file for pid
pid_file = '../pid/' + str(os.getpid())
common_file.common_file_save_data(pid_file, 'Musicbrainz_Sync', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Mbrainz Sync: Received USR1')
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
common_logging.com_logging_start('./log/MediaKraken_Subprogram_musicbrainz_Sync')


# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
    config_handle.get('DB Connections', 'PostDBPort').strip(),\
    config_handle.get('DB Connections', 'PostDBName').strip(),\
    config_handle.get('DB Connections', 'PostDBUser').strip(),\
    config_handle.get('DB Connections', 'PostDBPass').strip())


# open the remote musicbrainz db
db_brainz = database_base_brainz.srv_db_Brainz()
db_brainz.srv_db_open(config_handle.get('MediaBrainz', 'BrainzDBHost').strip(),\
    config_handle.get('MediaBrainz', 'BrainzDBPort').strip(),\
    config_handle.get('MediaBrainz', 'BrainzDBName').strip(),\
    config_handle.get('MediaBrainz', 'BrainzDBUser').strip(),\
    config_handle.get('MediaBrainz', 'BrainzDBPass').strip())

# log start
db.srv_db_activity_insert('MediaKraken_Server musicbrainz Start', None,\
    'System: Server musicbrainz Start', 'ServermusicbrainzStart', None, None, 'System')

# fetch all the artists from brainz
for row_data in db_brainz.srv_db_Brainz_All_Artists():
    db.srv_db_meta_musician_add(row_data['name'],\
        json.dumps({'musicbrainz':row_data['gid']}), json.dumps({'Comment':row_data['comment'],\
        'Gender':row_data['gender'], 'Begin':(str(row_data['begin_date_year']) + ':'\
        + str(row_data['begin_date_month']) + ':' + str(row_data['begin_date_day'])),\
        'End':(str(row_data['end_date_year']) + ':' + str(row_data['end_date_month']) + ':'\
        + str(row_data['end_date_day']))}))
    logging.debug(row_data)
    # fetch all the albums from brainz by artist
    for row_data_album in db_brainz.srv_db_Brainz_All_Albums_by_Artist(row_data['id']):
        db.srv_db_meta_album_add(row_data_album['name'],\
            json.dumps({'musicbrainz':row_data_album['gid']}),\
            json.dumps({'Commment':row_data_album['comment'],\
            'Language':row_data_album['language'], 'Barcode':row_data_album['barcode']}))
        logging.debug(row_data_album)
'''
        # fetch all the songs from brainz
        for row_data in db_brainz.srv_db_Brainz_All_Songs():
            # 0 gid, 1 name, 2 recording, 3 position, 4 id
            db.srv_db_meta_song_add(row_data[99],json.dumps({ 'musicbrainz':row_data[0] }),json.dumps({'':rowdata[99]}))
'''

# log end
db.srv_db_activity_insert('MediaKraken_Server musicbrainz Stop', None,\
    'System: Server musicbrainz Stop', 'ServermusicbrainzStop', None, None, 'System')

# commit all changes to db
db.srv_db_commit()
# close DB
db_brainz.srv_db_close()
db.srv_db_close()
# remove pid
os.remove(pid_file)
