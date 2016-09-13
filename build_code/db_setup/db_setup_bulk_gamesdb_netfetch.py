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
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("../../MediaKraken.ini")

import sys
import json
import xmltodict
sys.path.append("../../")
sys.path.append("../../common")
from common import common_metadata_gamesdb
import database as database_base

# import localization
import locale
locale.setlocale(locale.LC_ALL, '')

total_game_systems = 0
total_games = 0
# open the database
db = database_base.MKServerDatabase()
db.db_open(Config.get('DB Connections', 'PostDBHost').strip(),\
     Config.get('DB Connections', 'PostDBPort').strip(),\
     Config.get('DB Connections', 'PostDBName').strip(),\
     Config.get('DB Connections', 'PostDBUser').strip(),\
     Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.db_activity_insert('MediaKraken_Server theGamesDB Batch Start', None,\
    'System: Server theGamesDB Start', 'ServerthegamesDBStart', None, None, 'System')


gamesdb_connection = common_metadata_gamesdb.CommonMetadataGamesDB()

# grab and insert all platforms
for platform in gamesdb_connection.com_meta_gamesdb_platform_list():
    # fetch platform info
    platform_json\
        = xmltodict.parse(gamesdb_connection.com_meta_gamesdb_platform_by_id(platform.id))
    # store record
    db.db_meta_gamesdb_system_insert(platform.id, platform.name, platform.alias,\
        json.dumps(platform_json))
    # fetch all games for platform
    for game_data in xmltodict.parse(\
            gamesdb_connection.com_meta_gamesdb_games_by_platform_id(platform.id)):
        print("game_data %s", game_data)

# log end
db.db_activity_insert('MediaKraken_Server theGamesDB Batch Stop', None,\
    'System: Server theGamesDB Stop', 'ServerthegamesDBStop', None, None, 'System')


# send notications
if total_games > 0:
    db.db_notification_insert(locale.format('%d', total_games, True)\
        + " games(s) metadata added.", True)

if total_game_systems > 0:
    db.db_notification_insert(locale.format('%d', total_game_systems, True)\
        + " game system(s) metadata added.", True)


# commit all changes
db.db_commit()


# close DB
db.db_close()
