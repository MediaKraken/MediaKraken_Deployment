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
import json
import locale
locale.setlocale(locale.LC_ALL, '')
from common import common_config_ini
from common import common_logging
from common import common_metadata_anidb
from common import common_metadata_scudlee
from common import common_signal


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_AniDB_Updates')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server AniDB Update Start', None,\
    'System: Server AniDB Start', 'ServertheAniDBStart', None, None, 'System')


# stage totals
anime_added = 0
# grab the updated data
anidb = common_metadata_anidb.CommonMetadataANIdb(db_connection)
anidb.com_net_anidb_fetch_titles_file()
# insert into db
anidb.com_net_anidb_save_title_data_to_db()
# grab latest scudlee udpate
common_metadata_scudlee.mk_scudlee_fetch_xml()
# store the xref data
for anidbid, tvdbid, imdbid, default_tvseason in common_metadata_scudlee.mk_scudlee_anime_list_parse():
    logging.debug('ani %s, tv %s, imdb %s, default %s:', anidbid, tvdbid, imdbid, default_tvseason)
    db_connection.db_meta_anime_update_meta_id(json.dumps({'anidb': anidbid, 'thetvdb': tvdbid, 'imdb': imdbid, 'default': default_tvseason}))
# store the xref collection data
for scud_collection in common_metadata_scudlee.mk_scudlee_anime_set_parse():
    pass


# log end
db_connection.db_activity_insert('MediaKraken_Server AniDB Update Stop', None,\
    'System: Server AniDB Stop', 'ServertheAniDBStop', None, None, 'System')


# send notications
if anime_added > 0:
    db_connection.db_notification_insert(locale.format('%d', anime_added, True)\
        + " Anime metadata updated.", True)
    create_collection_trigger = True


# commit all changes
db_connection.db_commit()


# close DB
db_connection.db_close()
