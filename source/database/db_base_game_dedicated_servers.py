"""
  Copyright (C) 2020 Quinn D Granfor <spootdev@gmail.com>

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

import uuid


def db_game_server_insert(self, game_server_name, game_server_json):
    """
    insert game server
    """
    new_id = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_game_dedicated_servers (mm_game_server_guid,'
                           ' mm_game_server_name,'
                           ' mm_game_server_json)'
                           ' values (%s,%s,%s)',
                           (new_id, game_server_name, game_server_json))
    return new_id


def db_game_server_list_count(self):
    """
    Return number of game servers
    """
    self.db_cursor.execute('select count(*) from mm_game_dedicated_servers')
    return self.db_cursor.fetchone()[0]


def db_game_server_list(self, offset=0, records=None):
    """
    Return game server list
    """
    self.db_cursor.execute('select mm_game_server_guid,'
                           ' mm_game_server_name,'
                           ' mm_game_server_json'
                           ' from mm_game_dedicated_servers'
                           ' order by mm_game_server_name offset %s limit %s)', (offset, records))
    return self.db_cursor.fetchall()


def db_game_server_delete(self, record_uuid):
    """
    Delete game_server
    """
    self.db_cursor.execute('delete from mm_game_dedicated_servers'
                           ' where mm_game_server_guid = %s',
                           (record_uuid,))


def db_game_server_detail(self, record_uuid):
    """
    game server info
    """
    self.db_cursor.execute('select mm_game_server_name,'
                           ' mm_game_server_json'
                           ' from mm_game_dedicated_servers'
                           ' where mm_game_server_guid = %s', (record_uuid,))
    return self.db_cursor.fetchone()
