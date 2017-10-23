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
from common import common_config_ini
from common import common_metadata_thegamesdb

THEGAMESDB_CONNECTION = common_metadata_thegamesdb.CommonMetadataGamesDB()

def game_system_update():
    data = THEGAMESDB_CONNECTION.com_meta_gamesdb_platform_list()['Data']['Platforms']['Platform']
    print(type(data))
    print(data)
    for game_system in data:
        print(game_system)
        game_sys_detail = THEGAMESDB_CONNECTION.com_meta_gamesdb_platform_by_id(game_system['id'])['Data']['Platform']
        print(type(game_sys_detail))
        print(game_sys_detail)
        break