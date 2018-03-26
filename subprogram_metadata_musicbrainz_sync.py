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

import json
import logging  # pylint: disable=W0611

import db_base_brainz as database_base_brainz

from common import common_config_ini
from common import common_logging

# start logging
common_logging.com_logging_start(
    './log/MediaKraken_Subprogram_musicbrainz_Sync')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# open the remote musicbrainz db
db_brainz = database_base_brainz.db_Brainz()
db_brainz.db_open(option_config_json['MediaBrainz']['BrainzDBHost'],
                  option_config_json['MediaBrainz']['BrainzDBPort'],
                  option_config_json['MediaBrainz']['BrainzDBName'],
                  option_config_json['MediaBrainz']['BrainzDBUser'],
                  option_config_json['MediaBrainz']['BrainzDBPass'])

# log start
db_connection.db_activity_insert('MediaKraken_Server musicbrainz Start', None,
                                 'System: Server musicbrainz Start',
                                 'ServermusicbrainzStart', None,
                                 None, 'System')

# fetch all the artists from brainz
for row_data in db_brainz.db_brainz_all_artists():
    db_connection.db_meta_musician_add(row_data['name'],
                                       json.dumps(
                                           {'musicbrainz': row_data['gid']}),
                                       json.dumps({'Comment': row_data['comment'],
                                                   'Gender': row_data['gender'],
                                                   'Begin': (str(row_data['begin_date_year']) + ':'
                                                             + str(row_data[
                                                                       'begin_date_month']) + ':' + str(
                                                               row_data['begin_date_day'])),
                                                   'End': (str(
                                                       row_data['end_date_year']) + ':' + str(
                                                       row_data['end_date_month']) + ':'
                                                           + str(row_data['end_date_day']))}))
    logging.info(row_data)
    # fetch all the albums from brainz by artist
    for row_data_album in db_brainz.db_brainz_all_albums_by_artist(row_data['id']):
        db_connection.db_meta_album_add(row_data_album['name'],
                                        json.dumps(
                                            {'musicbrainz': row_data_album['gid']}),
                                        json.dumps({'Commment': row_data_album['comment'],
                                                    'Language': row_data_album['language'],
                                                    'Barcode': row_data_album['barcode']}))
        logging.info(row_data_album)
'''
        # fetch all the songs from brainz
        for row_data in db_brainz.db_Brainz_All_Songs():
            # 0 gid, 1 name, 2 recording, 3 position, 4 id
            db_connection.db_meta_song_add(row_data[99],json.dumps({ 'musicbrainz':row_data[0] }),json.dumps({'':rowdata[99]}))
'''

# log end
db_connection.db_activity_insert('MediaKraken_Server musicbrainz Stop', None,
                                 'System: Server musicbrainz Stop', 'ServermusicbrainzStop', None,
                                 None, 'System')

# commit all changes to db
db_connection.db_commit()

# vaccum tables that had records added
db_connection.db_pgsql_vacuum_table('mm_taketable')

# close DB
db_brainz.db_close()
db_connection.db_close()
