"""
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
"""

import json

from common import common_config_ini
from metadata import metadata_provider_thegamesdb

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

GAMESDB_INST = metadata_provider_thegamesdb.CommonMetadataGamesDB()

# grab and insert all platforms
for platform in \
        list(GAMESDB_INST.com_meta_gamesdb_platform_list()['Data']['Platforms'].items())[0]:
    if platform != 'Platform':
        for game_systems in platform:
            print(game_systems, flush=True)
            if db_connection.db_meta_games_system_guid_by_short_name(game_systems['name']) is None:
                # fetch platform info
                platform_json = GAMESDB_INST.com_meta_gamesdb_platform_by_id(game_systems['id'])
                # store record
                try:
                    system_alias = game_systems['alias']
                except KeyError:
                    system_alias = None
                db_connection.db_meta_games_system_insert(game_systems['id'],
                                                          game_systems['name'],
                                                          system_alias,
                                                          json.dumps(platform_json))
                db_connection.db_commit()


# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
