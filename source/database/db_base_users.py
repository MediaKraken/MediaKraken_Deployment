"""
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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


# class ServerDatabaseUsers:
def db_user_list_name_count(self):
    """
    # return user count
    """
    self.db_cursor.execute('select count(*) from mm_user')
    return self.db_cursor.fetchone()[0]


def db_user_profile_insert(self, profile_name, profile_json):
    """
    insert user profile
    """
    new_user_profile_id = uuid.uuid4()
    self.db_cursor.execute('insert into mm_user_profile (mm_user_profile_guid,'
                           ' mm_user_profile_name,'
                           ' mm_user_profile_json)'
                           ' values (%s, %s, %s)',
                           (new_user_profile_id, profile_name, profile_json))
    self.db_commit()
    return new_user_profile_id
