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
import uuid


# insert gamesdb game system
def MK_Server_Database_Metadata_GamesDB_System_Insert(self, platform_id, platform_name,\
        platform_alias, platform_json=None):
    self.sql3_cursor.execute('insert into mm_metadata_gamedb_systems_info(gsdb_id_pk, gsdb_game_system_id, gsdb_game_system_name, gsdb_game_system_alias, gsdb_game_system_json) values (%s, %s, %s, %s, %s)', (str(uuid.uuid4()), platform_id, platform_name, platform_alias, platform_json))
