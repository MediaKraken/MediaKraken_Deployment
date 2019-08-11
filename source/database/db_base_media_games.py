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


def db_media_game_system_list_count(self, search_value=None):
    """
    Audited system list count
    """
    pass


def db_media_game_system_list(self, offset=0, records=None, search_value=None):
    """
    Audited system list
    """
    pass


def db_media_game_list_by_system_count(self, system_id, search_value=None):
    """
    Audited game list by system count
    """
    pass


def db_media_game_list_by_system(self, system_id, offset=0, records=None, search_value=None):
    """
    Audited game list by system
    """
    pass


def db_media_game_list_count(self, search_value=None):
    """
    Audited games list count
    """
    pass


def db_media_game_list(self, offset=0, records=None, search_value=None):
    """
    Audited games list
    """
    pass


def db_media_mame_game_list(self):
    """
    Game systems are NULL for MAME
    """
    self.db_cursor.execute('select gi_id, gi_short_name from mm_game_info'
                           ' where gi_system_id is null and gi_gc_category is null')


def db_media_game_category_update(self, category, game_id):
    self.db_cursor.execute('update mm_game_info set gi_gc_category = %s'
                           ' where gi_id = %s', (category, game_id))
    self.db_cursor.commit()


def db_media_game_clone_list(self):
    self.db_cursor.execute('select gi_id, gi_cloneof from mm_game_info'
                           ' where gi_system_id is null'
                           ' and gi_cloneof IS NOT NULL and gi_gc_category is null')
    return self.db_cursor.fetchall()


def db_media_game_category_by_name(self, category_name):
    self.db_cursor.execute('select gi_gc_category from mm_game_info'
                           ' where gi_short_name = %s', (category_name,))
    return self.db_cursor.fetchone()[0]
